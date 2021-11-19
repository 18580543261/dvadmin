import hashlib

from django.contrib import auth
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.views import APIView

from apps.dvadmin.system.models import Users
from plugins.dvadmin_mqtt_iot.models import DeviceModel
from plugins.user.models import ECaptchaModel
from utils.apps.dvadmin.json_response import SuccessResponse, ErrorResponse
from utils.apps.dvadmin.serializers import CustomModelSerializer
from utils.apps.dvadmin.viewset import CustomModelViewSet


class ApiLoginView(APIView):
    """接口文档的登录接口"""
    authentication_classes = []
    permission_classes = []

    def login_password(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            password = password.encode(encoding='UTF-8')
            user_obj = auth.authenticate(request, email=email, password=hashlib.md5(password).hexdigest())
        except Exception:
            user_obj = None

        if user_obj:
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    def login_ecaptcha(self, request):
        email = request.data.get('email')
        ecaptcha = request.data.get('ecaptcha')
        try:
            obj = ECaptchaModel.objects.get(email=email,ecaptcha=ecaptcha)
        except Exception:

            return ErrorResponse(msg='')
        else:
            return HttpResponse(status=status.HTTP_200_OK)