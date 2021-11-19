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
system_url.register(r'mqtt/disconnect', DisConnectViewSet)
system_url.register(r'mqtt/publish', PublishViewSet)
system_url.register(r'mqtt/deliver', DeliverViewSet)
system_url.register(r'mqtt/ack', AckViewSet)
system_url.register(r'mqtt/drop', DropViewSet)
system_url.register(r'mqtt/subscribe', SubscribeViewSet)
system_url.register(r'mqtt/unsubscribe', UnSubscribeViewSet)
system_url.register(r'device', DeviceViewSet)

urlpatterns = [
    path('device/get_defualt/',DeviceViewSet.as_view({'post': 'get_defualt'})),

    path('mqtt/login/',ConnectLoginView.as_view()),
    path('mqtt/is_superuser/',IsSuperUserView.as_view()),
    path('mqtt/can_publish/',CanPublishView.as_view()),
]
urlpatterns += system_url.urls