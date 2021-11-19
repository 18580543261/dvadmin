# -*- coding: utf-8 -*-
from django.urls import path, re_path
from rest_framework import routers

from plugins.dvadmin_mqtt_iot.views.device import DeviceViewSet
from plugins.dvadmin_mqtt_iot.views.mqtt import ConnectViewSet, ConnectLoginView, IsSuperUserView, CanPublishView
from plugins.dvadmin_mqtt_iot.views.mqtt import DisConnectViewSet
from plugins.dvadmin_mqtt_iot.views.mqtt import DeliverViewSet
from plugins.dvadmin_mqtt_iot.views.mqtt import AckViewSet
from plugins.dvadmin_mqtt_iot.views.mqtt import SubscribeViewSet
from plugins.dvadmin_mqtt_iot.views.mqtt import UnSubscribeViewSet
from plugins.dvadmin_mqtt_iot.views.mqtt import DropViewSet
from plugins.dvadmin_mqtt_iot.views.mqtt import PublishViewSet

system_url = routers.SimpleRouter()
system_url.register(r'mqtt/connect', ConnectViewSet)

urlpatterns = [
    path('device/get_defualt/',DeviceViewSet.as_view({'post': 'get_defualt'}))
]
urlpatterns += system_url.urls