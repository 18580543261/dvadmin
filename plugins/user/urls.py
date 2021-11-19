# -*- coding: utf-8 -*-
from django.urls import path, re_path
from rest_framework import routers

system_url = routers.SimpleRouter()
# system_url.register(r'mqtt/connect', ConnectViewSet)

urlpatterns = [
]
urlpatterns += system_url.urls