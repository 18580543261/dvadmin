# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/2 002 14:20
@Remark:登录视图
"""
import base64
import hashlib
from datetime import timedelta

from captcha.views import CaptchaStore, captcha_image
from django.contrib import auth
from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.dvadmin.system.models import Users, ECaptchaStore
from utils.apps.dvadmin.json_response import SuccessResponse, ErrorResponse
from utils.apps.dvadmin.serializers import CustomModelSerializer
from utils.apps.dvadmin.validator import CustomValidationError

class CaptchaView(APIView):
    authentication_classes = []

    @swagger_auto_schema(
        responses={
            '200': openapi.Response('获取成功')
        },
        security=[],
        operation_id='captcha-get',
        operation_description='验证码获取',
    )
    def get(self, request):
        hashkey = CaptchaStore.generate_key()
        id = CaptchaStore.objects.filter(hashkey=hashkey).first().id
        imgage = captcha_image(request, hashkey)
        # 将图片转换为base64
        image_base = base64.b64encode(imgage.content)
        json_data = {"key": id, "image_base": "data:image/png;base64," + image_base.decode('utf-8')}
        return SuccessResponse(data=json_data)

class ECaptchaView(APIView):
    authentication_classes = []

    @swagger_auto_schema(
        responses={
            '200': openapi.Response('获取成功')
        },
        security=[],
        operation_id='ecaptcha-get',
        operation_description='e验证码获取',
    )
    def post(self, request):
        email = request.data.get('email')#email
        try:
            obj = Users.objects.get(email=email)
        except Users.DOESNOT_EXIST:
            return ErrorResponse(msg='账号不存在')
        else:
            expire = 1 * 60
            objEmail = ECaptchaStore(expire=expire, email=email)
            objEmail.save()
            return SuccessResponse(data={"expire":expire,"unit":"秒"})


class LoginSerializer(TokenObtainPairSerializer):
    """
    登录的序列化器:
    重写djangorestframework-simplejwt的序列化器
    """
    # captcha = serializers.CharField(max_length=6)
    username_field = get_user_model().EMAIL_FIELD
    code = serializers.CharField(max_length=6,allow_blank=True,allow_null=True)

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]

    default_error_messages = {
        'no_active_account': _('该账号已被禁用,请联系管理员')
    }

    # def validate_captcha(self, captcha):
    #     self.image_code = CaptchaStore.objects.filter(
    #         id=self.initial_data['captchaKey']).first()
    #     five_minute_ago = timezone.now() - timedelta(hours=0, minutes=5, seconds=0)
    #     if self.image_code and five_minute_ago > self.image_code.expiration:
    #         self.image_code and self.image_code.delete()
    #         raise CustomValidationError('验证码过期')
    #     else:
    #         if self.image_code and (self.image_code.response == captcha or self.image_code.challenge == captcha):
    #             self.image_code and self.image_code.delete()
    #         else:
    #             self.image_code and self.image_code.delete()
    #             raise CustomValidationError("图片验证码错误")

    def validate(self, attrs):
        print('LoginSerializer:attrs:',attrs)
        email = attrs['email']
        password = attrs['password']
        code = attrs['code']
        print('LoginSerializer:code:',code)
        print('LoginSerializer:password:',password)
        user = Users.objects.filter(email=email).first()
        if user and user.check_password(password):  # check_password() 对明文进行加密,并验证
            data = super().validate(attrs)
            refresh = self.get_token(self.user)

            data['name'] = self.user.name
            data['userId'] = self.user.id
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            data['username'] = self.user.username
            data['nickname'] = self.user.name
            data['phone'] = self.user.mobile
            data['avatar'] = ''
            result = {
                "code": 2000,
                "msg": "请求成功",
                "data": data
            }
        else:
            result = {
                "code": 4000,
                "msg": "账号/密码不正确",
                "data": None
            }
        return result


class LoginView(TokenObtainPairView):
    """
    登录接口
    """
    serializer_class = LoginSerializer
    permission_classes = []


class ApiLoginSerializer(CustomModelSerializer):
    """接口文档登录-序列化器"""
    email = serializers.CharField()
    password = serializers.CharField()
    code = serializers.CharField()

    class Meta:
        model = Users
        fields = ['code','email','password']



class ApiLogin(APIView):
    """接口文档的登录接口"""
    serializer_class = ApiLoginSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            password = password.encode(encoding='UTF-8')
            user_obj = auth.authenticate(request, username=username, password=hashlib.md5(password).hexdigest())
        except Exception:
            user_obj = None

        if user_obj:
            print('登录成功')
            login(request,user_obj)
            return redirect('/')
        else:
            print('登录失败')
            return ErrorResponse(msg="账号/密码错误")
