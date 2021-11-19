from rest_framework import serializers
from rest_framework.views import APIView

from plugins.dvadmin_mqtt_iot.models import DeviceModel, CellModel, CellValueModel
from utils.apps.dvadmin.json_response import SuccessResponse, ErrorResponse
from utils.apps.dvadmin.serializers import CustomModelSerializer
from utils.apps.dvadmin.viewset import CustomModelViewSet


class CellValueSerializer(CustomModelSerializer):
    type_ = serializers.SerializerMethodField(read_only=True)

    def get_type_(self, instance):
        return instance.get_type_display()
    """定时任务 序列化器"""
    class Meta:
        model = CellValueModel
        fields = "__all__"


class CellSerializer(CustomModelSerializer):
    cellvalue = CellValueSerializer(many=True, read_only=True)
    type_ = serializers.SerializerMethodField(read_only=True)

    def get_type_(self, instance):
        return instance.get_type_display()
    """定时任务 序列化器"""
    class Meta:
        model = CellModel
        fields = "__all__"



class DeviceSerializer(CustomModelSerializer):
    cell = CellSerializer(many=True, read_only=True)
    type_ = serializers.SerializerMethodField(read_only=True)
    status_ = serializers.SerializerMethodField(read_only=True)

    def get_type_(self, instance):
        return instance.get_type_display()
    def get_status_(self, instance):
        return instance.get_status_display()
    """定时任务 序列化器"""
    class Meta:
        model = DeviceModel
        fields = "__all__"


class DeviceViewSet(CustomModelViewSet):
    serializer_class = DeviceSerializer
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
