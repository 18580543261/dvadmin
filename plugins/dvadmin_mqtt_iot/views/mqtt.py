# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/8/22 022 10:16
@Remark:
"""
import datetime
import hashlib
import json
import re
import time
import traceback
import uuid

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, _get_queryset
from django.utils import timezone
from rest_framework.views import APIView

from apps.dvadmin.system.models import Users
from plugins.dvadmin_mqtt_iot.models import ConnectModel, DisConnectModel, DeliverModel, AckModel, SubscribeModel, \
    UnSubscribeModel, Base, DropModel, DeviceModel, CellModel, CellValueModel
from utils.apps.dvadmin.json_response import SuccessResponse, ErrorResponse
from utils.apps.dvadmin.serializers import CustomModelSerializer
from utils.apps.dvadmin.viewset import CustomModelViewSet

from rest_framework import serializers, status


class MqttModelSerializer(CustomModelSerializer):
    pass
    # timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    # disconnected_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

class ConnectSerializer(MqttModelSerializer):
    """定时任务 序列化器"""
    class Meta:
        model = ConnectModel
        fields = "__all__"

class DisConnectSerializer(MqttModelSerializer):
    """定时任务 序列化器"""
    class Meta:
        model = DisConnectModel
        fields = "__all__"

class DeliverSerializer(MqttModelSerializer):
    """定时任务 序列化器"""
    class Meta:
        model = DeliverModel
        fields = "__all__"

class AckSerializer(MqttModelSerializer):
    """定时任务 序列化器"""
    class Meta:
        model = AckModel
        fields = "__all__"

class DropSerializer(MqttModelSerializer):
    """定时任务 序列化器"""
    class Meta:
        model = DropModel
        fields = "__all__"

class SubscribeSerializer(MqttModelSerializer):
    """定时任务 序列化器"""
    class Meta:
        model = SubscribeModel
        fields = "__all__"

class UnSubscribeSerializer(MqttModelSerializer):
    """定时任务 序列化器"""
    class Meta:
        model = UnSubscribeModel
        fields = "__all__"


class MQTTViewSet(CustomModelViewSet):
    type = 'default'
    lookup_field = 'clientid'
    keywords = ['clientid']

    def get_object_(self,kwargs=None):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        kwargs = kwargs if kwargs else self.kwargs
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {**kwargs}
        obj = get_object_or_404(queryset,**filter_kwargs)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        data = request.data
        data.setdefault('dept_belong_id', getattr(request.user, 'dept_id', None))
        data = self.from_data(data)
        for kwarg in self.keywords:
            kwargs.setdefault(kwarg, data.get(kwarg))
        try:
            res = self.update_(request,data,**kwargs)
        except Http404 as e:
            print(e)
            res = self.create_(request,data)
        self.onMqtt(data)
        return res

    def onMqtt(self,data):
        pass

    def create_(self, request, data, **kwargs):
        serializer = self.get_serializer(data=data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return SuccessResponse(data=serializer.data, msg="新增成功")

    def update_(self, request, data, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object_(kwargs)
        serializer = self.get_serializer(instance, data=data, request=request, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return SuccessResponse(data=serializer.data, msg="更新成功")



    def from_data(self,data):
        instance = {}

        for k, v in data.items():
            v = json.dumps(v) if isinstance(v, dict) else v
            k = '_id' if k == 'id' else k
            v = True if v == 'true' else v
            v = False if v == 'false' else v
            if k in ['timestamp'] or k.endswith('_at'):
                v = datetime.datetime.fromtimestamp(v / 1000)
                v = timezone.make_aware(v)
            instance.setdefault(k, v)
        return instance


class ConnectViewSet(MQTTViewSet):
    queryset = ConnectModel.objects.all()
    serializer_class = ConnectSerializer
    filter_fields = []

    def onMqtt(self,data):
        print('上线通知,设备',data.get("clientid"))
        try:
            device = DeviceModel.objects.get(id=data.get('clientid'))
        except DeviceModel.DoesNotExist:
            print(f'设备{data.get("clientid")}不存在')
        else:
            device.status = 1
            device.save()

class DisConnectViewSet(MQTTViewSet):
    queryset = DisConnectModel.objects.all()
    serializer_class = DisConnectSerializer
    filter_fields = []

    def onMqtt(self,data):
        print('离线通知,设备',data.get("clientid"))
        try:
            device = DeviceModel.objects.get(id=data.get('clientid'))
        except DeviceModel.DoesNotExist:
            print(f'设备{data.get("clientid")}不存在')
        else:
            device.status = 0
            device.save()

class PublishViewSet(MQTTViewSet):
    queryset = DeliverModel.objects.all()
    serializer_class = DeliverSerializer
    filter_fields = []

    def create(self, request, *args, **kwargs):
        print(self.__class__.__name__)
        print(request.body)
        pass


class DeliverViewSet(MQTTViewSet):
    queryset = DeliverModel.objects.all()
    serializer_class = DeliverSerializer
    filter_fields = []

    def create(self, request, *args, **kwargs):
        data = self.from_data(request.data)
        serializer = self.get_serializer(data=data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        topic = data.get('topic')
        username = data.get('username')
        clientid = data.get('clientid')
        if re.match(f'{username}/{clientid}/regist/',topic):
            self.on_regist(request.user,data)
        elif re.match(f'{username}/{clientid}/control/',topic):
            self.on_control(request.user,data)
        elif re.match(f'{username}/{clientid}/status/',topic):
            self.on_status(request.user,data)
        elif re.match(f'{username}/{clientid}/gap/',topic):
            self.on_status(request.user,data)
        return SuccessResponse(data=serializer.data, msg="新增成功")

    def on_status(self,user,data):
        print('元件状态',data)
        clientid = data.get('clientid')
        payload = data.get('payload')
        payload = dict(json.loads(payload))
        try:
            device = DeviceModel.objects.get(id=clientid)
            user = device.creator
        except DeviceModel.DoesNotExist:
            return
        try:
            cell = CellModel.objects.get(clientid=device, code=payload.get('code'),type=payload.get('type'))
        except CellModel.DoesNotExist:
            return

        cvalue = CellValueModel()
        cvalue.type, xxx = CellValueModel.TYPE_CHOICES[1]
        cvalue.value = payload.get('data')
        cvalue.creator = user
        cvalue.cellid = cell
        cvalue.save()

    def on_control(self,user,data):
        print('控制元件',data)
        clientid = data.get('clientid')
        payload = data.get('payload')
        payload = dict(json.loads(payload))
        try:
            device = DeviceModel.objects.get(id=clientid)
            user = device.creator
        except DeviceModel.DoesNotExist:
            return
        try:
            cell = CellModel.objects.get(clientid=device,code=payload.get('code'),type=payload.get('type'))
        except CellModel.DoesNotExist:
            return
        cvalue = CellValueModel()
        cvalue.type, xxx = CellValueModel.TYPE_CHOICES[0]
        cvalue.value = payload.get('data')
        cvalue.creator = user
        cvalue.cellid = cell
        cvalue.save()


    def on_regist(self,user,data):
        print('注册元件',data)
        clientid = data.get('clientid')
        payload = data.get('payload')
        payload = dict(json.loads(payload))
        cells_data = payload.get('data', [])
        for cell_ in cells_data:
            try:
                device = DeviceModel.objects.get(id=clientid)
                user = device.creator
            except DeviceModel.DoesNotExist:
                return None
            try:
                cell = CellModel.objects.get(clientid=device, code=cell_.get('code'),type=cell_.get('type'))
            except CellModel.DoesNotExist:
                cell = CellModel()
                cell.clientid = device
                cell.creator = user
                cell.type = cell_.get('type')
                cell.code = cell_.get('code')
                cell.save()

    def on_gap(self,user,data):
        print('控制频率',data)
        clientid = data.get('clientid')
        payload = data.get('payload')
        payload = dict(json.loads(payload))
        try:
            device = DeviceModel.objects.get(id=clientid)
        except DeviceModel.DoesNotExist:
            return
        try:
            cell = CellModel.objects.get(clientid=device, code=payload.get('code'),type=payload.get('type'))
        except CellModel.DoesNotExist:
            return
        else:
            cell.gap = payload.get('data')
            cell.save()


class AckViewSet(MQTTViewSet):
    queryset = AckModel.objects.all()
    serializer_class = AckSerializer
    filter_fields = []


class DropViewSet(MQTTViewSet):
    queryset = DropModel.objects.all()
    serializer_class = DropSerializer
    filter_fields = []


class SubscribeViewSet(MQTTViewSet):
    queryset = SubscribeModel.objects.all()
    serializer_class = SubscribeSerializer
    filter_fields = []
    keywords = ['clientid','topic']


class UnSubscribeViewSet(MQTTViewSet):
    queryset = UnSubscribeModel.objects.all()
    serializer_class = UnSubscribeSerializer
    filter_fields = []
    keywords = ['clientid','topic']



class ConnectLoginView(APIView):
    """接口文档的登录接口"""
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        clientid = request.data.get('clientid')
        try:
            DeviceModel.objects.get(id=clientid)
        except DeviceModel.DoesNotExist:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED,content='clientid不允许')
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            password = password.encode(encoding='UTF-8')
            user_obj = auth.authenticate(request, username=username, password=hashlib.md5(password).hexdigest())
        except Exception:
            user_obj = None
        if not user_obj:
            try:
                validated_token = self.get_validated_token(password)
                print('validated_token',validated_token)
                user_obj = self.get_user(validated_token)
            except Exception:
                user_obj = None
        if user_obj:
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        from rest_framework_simplejwt.settings import api_settings
        from rest_framework_simplejwt.exceptions import TokenError
        from rest_framework_simplejwt.exceptions import InvalidToken
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append({'token_class': AuthToken.__name__,
                                 'token_type': AuthToken.token_type,
                                 'message': e.args[0]})

        raise InvalidToken({
            'detail': 'Given token not valid for any token type',
            'messages': messages,
        })

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """

        from rest_framework_simplejwt.settings import api_settings
        from rest_framework_simplejwt.exceptions import AuthenticationFailed
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            from rest_framework_simplejwt.exceptions import InvalidToken
            raise InvalidToken('Token contained no recognizable user identification')

        try:
            user = get_user_model().objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.get_user_model().DoesNotExist:
            raise AuthenticationFailed('User not found', code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed('User is inactive', code='user_inactive')

        return user

class IsSuperUserView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        clientid = request.data.get('clientid')
        username = request.data.get('username')
        user_obj = Users.objects.filter(username=username, is_superuser=True)
        if user_obj:
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


class CanPublishView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        access = request.data.get('access')
        username = request.data.get('username')
        clientid = request.data.get('clientid')
        ipaddr = request.data.get('ipaddr')
        topic = request.data.get('topic')
        print('CanPublishView:',request.data)
        user_obj = False

        if re.match(f'{username}/.*',topic):
            user_obj = True


        if user_obj:
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
