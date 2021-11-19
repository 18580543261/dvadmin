# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/1 001 23:05
@Remark: 系统管理的路由文件
"""
from django.urls import path, re_path
from rest_framework import routers

from apps.dvadmin.system.views.area import AreaViewSet
from apps.dvadmin.system.views.button import ButtonViewSet
from apps.dvadmin.system.views.dept import DeptViewSet
from apps.dvadmin.system.views.dictionary import DictionaryViewSet
from apps.dvadmin.system.views.file_list import FileViewSet
from apps.dvadmin.system.views.img_list import ImgViewSet
from apps.dvadmin.system.views.menu import MenuViewSet
from apps.dvadmin.system.views.menu_button import MenuButtonViewSet
from apps.dvadmin.system.views.operation_log import OperationLogViewSet
from apps.dvadmin.system.views.role import RoleViewSet
from apps.dvadmin.system.views.user import UserViewSet

system_url = routers.SimpleRouter()
system_url.register(r'menu', MenuViewSet)
system_url.register(r'button', ButtonViewSet)
system_url.register(r'menu_button', MenuButtonViewSet)
system_url.register(r'role', RoleViewSet)
system_url.register(r'dept', DeptViewSet)
system_url.register(r'user', UserViewSet)
system_url.register(r'operation_log', OperationLogViewSet)
system_url.register(r'dictionary', DictionaryViewSet)
system_url.register(r'area', AreaViewSet)
system_url.register(r'img', ImgViewSet)
system_url.register(r'file', FileViewSet)

urlpatterns = [
    re_path('role/role_id_to_menu/(?P<pk>.*?)/', RoleViewSet.as_view({'get': 'roleId_to_menu'})),
    path('menu/web_router/', MenuViewSet.as_view({'get': 'web_router'})),
    path('user/user_info/', UserViewSet.as_view({'get': 'user_info', 'put': 'update_user_info'})),
    re_path('user/change_password/(?P<pk>.*?)/', UserViewSet.as_view({'put': 'change_password'})),
]
urlpatterns += system_url.urls
