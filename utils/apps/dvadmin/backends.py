import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone

logger = logging.getLogger(__name__)
UserModel = get_user_model()


class CustomBackend(ModelBackend):
    """
    Django原生认证方式
    """

    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        msg = '%s 正在使用本地登录...' % username
        logger.info(msg)
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if email is None:
            email = kwargs.get(UserModel.EMAIL_FIELD)
        try:
            if username:
                user = UserModel._default_manager.get_by_natural_key(username)
            elif email:
                user = UserModel._default_manager.get(email=email)
            else:
                raise Exception('email or username are not available')
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                user.last_login = timezone.now()
                user.save()
                return user
