# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/8/22 022 19:23
@Remark:
"""
import uuid

from django.conf import settings
from django.db import models

from utils.apps.dvadmin.models import CoreModel


def defaultDict():
    return {}


class ECaptchaModel(CoreModel):

    captcha = models.CharField(max_length=20,default=uuid.uuid4(), verbose_name="验证码", help_text="验证码")
    email = models.CharField(max_length=20,default='', verbose_name="邮箱", help_text="邮箱")
    tryn = models.IntegerField(default=0, verbose_name="尝试次数", help_text="尝试次数")
    expire = models.IntegerField(default=1 * 60, verbose_name="有效时间", help_text="有效时间")

    class Meta:
        db_table = settings.TABLE_PREFIX + "user_ecaptcha"
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)


