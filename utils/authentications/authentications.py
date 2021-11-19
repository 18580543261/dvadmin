import pickle
import sys

from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BaseAuthentication

import datetime
from django.utils import timezone
from django.utils.translation import ugettext_lazy
from django.core.cache import cache
from rest_framework import exceptions, HTTP_HEADER_ENCODING
from rest_framework.authtoken.models import Token


#绕过csrf验证，不建议采用
class UnSCRFAuthenticated(SessionAuthentication):
    def authenticate(self, request):
        user = getattr(request._request, 'user', None)
        self.enforce_csrf(request)
        return (user, None)
    def enforce_csrf(self, request):
        pass

# token验证
class ExpiringTokenAuthentication(BaseAuthentication):
    model = Token

    def authenticate(self, request):
        print(f'{sys._getframe().f_code.co_name} is called!')
        auth = self.get_authorization_header(request)
        if not auth:
            print('ExpiringTokenAuthentication: not auth')
            return None
        try:
            token = auth.decode()
        except UnicodeError:
            msg = ugettext_lazy("无效的Token， Token头不应包含无效字符")
            print(msg)
            raise exceptions.AuthenticationFailed(msg)
        return self.authenticate_credentials(token)

    def enforce_csrf(self, request):
        pass

    def authenticate_credentials(self, key):
        # 尝试从缓存获取用户信息（设置中配置了缓存的可以添加，不加也不影响正常功能）
        token_cache = 'token_' + key
        cache_user = cache.get(token_cache)
        # if cache_user:
        #     cache_user = pickle.loads(cache_user)
        #     print('authenticate_credentials:cache_user: ', cache_user)
        #     return cache_user, cache_user  # 这里需要返回一个列表或元组，原因不详
        # 缓存获取到此为止
        # 下面开始获取请求信息进行验证
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            print('authenticate_credentials','认证失败')
            raise exceptions.AuthenticationFailed("认证失败")
        if not token.user.is_active:
            print('authenticate_credentials','用户被禁用')
        # Token有效期时间判断（注意时间时区问题）
        # 我在设置里面设置了时区 USE_TZ = False，如果使用utc这里需要改变。
        cache_expire = 7*24*60*60
        if (timezone.now() - token.created) > datetime.timedelta(seconds=cache_expire):
            print('authenticate_credentials','认证信息已过期')
            raise exceptions.AuthenticationFailed('认证信息已过期')
        # 加入缓存增加查询速度，下面和上面是配套的，上面没有从缓存中读取，这里就不用保存到缓存中了
        if token:
            cache.set(token_cache, pickle.dumps(token.user), cache_expire)
        # 返回用户信息
        return token.user, token.user

    def authenticate_header(self, request):
        return 'Token'

    def get_authorization_header(self,request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if isinstance(auth, type('')):
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

# 表示登录了
class LoginAuthenticated(UnSCRFAuthenticated):
    def authenticate(self, request):
        user = getattr(request._request, 'user', None)
        if not user or not user.is_authenticated:
            return None
        self.enforce_csrf(request)
        return (user, None)


# 表示登录过，但未激活了账户
class UnActiveAuthenticated(UnSCRFAuthenticated):
    def authenticate(self, request):
        user = getattr(request._request, 'user', None)
        if (not user or not user.is_authenticated) or user.is_active:
            return None
        self.enforce_csrf(request)
        return (user, None)


# 表示登录过，而且激活了账户
class ActiveAuthenticated(UnSCRFAuthenticated):
    def authenticate(self, request):
        user = getattr(request._request, 'user', None)
        if not user or not user.is_active:
            return None
        self.enforce_csrf(request)
        return (user, None)


# 表示未登录
class UnLoginAuthenticated(UnSCRFAuthenticated):
    def authenticate(self, request):
        user = getattr(request._request, 'user', None)
        if user and user.is_authenticated:
            return None
        self.enforce_csrf(request)
        return (user, None)
