from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from plugins.dvadmin_mqtt_iot.models import DeviceModel, CellModel, CellValueModel
from plugins.wxlogin.models import WxUser
from utils.apps.dvadmin.json_response import SuccessResponse, ErrorResponse
from utils.apps.dvadmin.serializers import CustomModelSerializer
from utils.apps.dvadmin.viewset import CustomModelViewSet


class JfwTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(JfwTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = 'wx_{0}'.format(user.username)
        return token


class DeviceViewSet(CustomModelViewSet):
    serializer_class = WxSerializer
    queryset = DeviceModel.objects.all()
    filter_fields = []

    def get_defualt(self,request, *arg, **kwargs):
        serial = request.data.get('serial',None)
        type = request.data.get('type',0)
        if serial is None:
            return ErrorResponse(msg='序列号为空')

        try:
            obj = DeviceModel.objects.get(serial=serial)
        except DeviceModel.DoesNotExist:
            obj = DeviceModel()
            obj.creator = request.user
            obj.serial = serial
            obj.type = type
            obj.save()
        id = obj.id
        return SuccessResponse(data={'clientid':id})
