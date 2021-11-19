# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/8/22 022 19:23
@Remark:
"""
import datetime
import json
import uuid

from django.db import models
from django.db.models import JSONField
from django.utils import timezone

from django.conf import settings
from utils.apps.dvadmin.models import CoreModel

def defaultDict():
    return {}


class DeviceModel(CoreModel):
    STATUS_CHOICES = ((0, "离线"), (1, "在线"))
    TYPE_CHOICES = ((0, '设备'),(1, "前端"))
    serial = models.CharField(max_length=255,default=uuid.uuid4, verbose_name="序列号", help_text="序列号")
    status = models.IntegerField(default=0, choices=STATUS_CHOICES, verbose_name="设备状态", help_text="设备状态")
    type = models.IntegerField(default=0, choices=TYPE_CHOICES, verbose_name="设备类型", help_text="设备类型")

    class Meta:
        db_table = settings.TABLE_PREFIX + "iot_device"
        verbose_name = '物联网设备'
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)


class CellModel(CoreModel):
    TYPE_CHOICES = (
        ('lamp', '灯'),
        ('sensor_temperature', "温度传感器"),
        ('sensor_moisture', "湿度传感器"),
        ('sensor_gravity', "重力传感器"),
        ('driver', "驱动电机"),
    )
    type = models.CharField(max_length=32,default='lamp', choices=TYPE_CHOICES, verbose_name="类型", help_text="元件类型")
    code = models.IntegerField(default=0, verbose_name="编号", help_text="编号")
    gap = models.IntegerField(default=1000*60, verbose_name="上传间隔毫秒", help_text="上传间隔毫秒")
    clientid = models.ForeignKey(to=DeviceModel, null=True,related_name='cell',
                                 verbose_name='设备名称', help_text="设备名称", on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = settings.TABLE_PREFIX + "iot_cell"
        verbose_name = '物联网设备-元件'
        verbose_name_plural = verbose_name
        ordering = ('type','create_datetime')


class CellValueModel(CoreModel):
    TYPE_CHOICES = (
        ('control', '控制'),
        ('status', "状态")
    )
    type = models.CharField(max_length=32,default='status', choices=TYPE_CHOICES, verbose_name="类型", help_text="类型")
    value = models.CharField(max_length=5,default='', verbose_name="当前值", help_text="当前值")
    cellid = models.ForeignKey(to=CellModel, null=True,related_name='cellvalue',
                                 verbose_name='元件', help_text="元件", on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = settings.TABLE_PREFIX + "iot_cvalue"
        verbose_name = '物联网设备-元件值'
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)

class Base(CoreModel):
    username = models.CharField(max_length=255,default='')
    timestamp = models.DateTimeField(blank=True, null=True)
    clientid = models.ForeignKey(to=DeviceModel, null=True,
                                verbose_name='设备名称', help_text="设备名称", on_delete=models.CASCADE, db_constraint=False)
    node = models.CharField(max_length=255,default='')
    metadata = models.JSONField(default=defaultDict)
    event = models.CharField(max_length=255,default='')

    class Meta:
        abstract = True


class BaseTopic(Base):
    topic = models.CharField(max_length=255,default='')
    qos = models.IntegerField(default=0)
    peerhost = models.CharField(max_length=255,default='')

    class Meta:
        abstract = True


class ConnectModel(Base):
    sockname = models.CharField(max_length=255,default='')
    receive_maximum = models.CharField(max_length=255,default='')
    proto_ver = models.IntegerField(default=0)
    proto_name = models.CharField(max_length=255,default='')
    peername = models.CharField(max_length=255,default='')
    mountpoint = models.CharField(max_length=255,default='')
    keepalive = models.IntegerField(default=0)
    is_bridge = models.BooleanField(default=False)
    expiry_interval = models.IntegerField(default=0)
    connected_at = models.DateTimeField(blank=True, null=True)
    conn_props = models.JSONField(default=defaultDict)
    clean_start = models.BooleanField(default=True)

    class Meta:
        db_table = settings.TABLE_PREFIX + "iot_mqtt_connect"
        verbose_name = '设备连接'
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)


class DisConnectModel(Base):
    sockname = models.CharField(max_length=255,default='')
    reason = models.CharField(max_length=255,default='')
    peername = models.CharField(max_length=255,default='')
    disconnected_at = models.DateTimeField(blank=True, null=True)
    disconn_props = models.JSONField(default=defaultDict)

    class Meta:
        db_table = settings.TABLE_PREFIX + "iot_mqtt_disconnect"
        verbose_name = '设备断开'
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)


class DeliverModel(BaseTopic):
    sub_props = models.CharField(max_length=255,default='')
    publish_received_at = models.DateTimeField(blank=True, null=True)
    payload = models.CharField(max_length=255,default='')
    _id = models.CharField(max_length=255,default='')
    headers = models.JSONField(default=defaultDict)
    from_username = models.CharField(max_length=255,default='')
    from_clientid = models.CharField(max_length=255,default='')
    flags = models.JSONField(default=defaultDict)

    class Meta:
        db_table = settings.TABLE_PREFIX + "iot_mqtt_deliver"
        verbose_name = '消息发布'
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)


class AckModel(BaseTopic):
    publish_received_at = models.DateTimeField(blank=True, null=True)
    pub_props = models.CharField(max_length=255,default='')
    puback_props = models.CharField(max_length=255,default='')
    payload = models.CharField(max_length=255,default='')
    _id = models.CharField(max_length=255,default='')
    headers = models.CharField(max_length=255,default='')
    from_username = models.CharField(max_length=255,default='')
    from_clientid = models.CharField(max_length=255,default='')
    flags = models.CharField(max_length=255,default='')

    class Meta:
        db_table = settings.TABLE_PREFIX + "iot_mqtt_ack"
        verbose_name = '消息应答'
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)


class DropModel(BaseTopic):
    publish_received_at = models.DateTimeField(blank=True, null=True)
    pub_props = models.CharField(max_length=255, default='')
    payload = models.CharField(max_length=255, default='')
    _id = models.CharField(max_length=255, default='')
    headers = models.CharField(max_length=255, default='')
    flags = models.CharField(max_length=255, default='')
    reason = models.CharField(max_length=255, default='')

    class Meta:
        db_table = settings.TABLE_PREFIX + "iot_mqtt_drop"
        verbose_name = '消息丢弃'
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)


class SubscribeModel(BaseTopic):
    pub_props = models.CharField(max_length=255,default='')

    class Meta:
        db_table = settings.TABLE_PREFIX + "iot_mqtt_subscribe"
        verbose_name = '主题订阅'
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)


class UnSubscribeModel(BaseTopic):
    unsub_props = models.CharField(max_length=255,default='')

    class Meta:
        db_table = settings.TABLE_PREFIX + "iot_mqtt_unsubscribe"
        verbose_name = '取消订阅'
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)



