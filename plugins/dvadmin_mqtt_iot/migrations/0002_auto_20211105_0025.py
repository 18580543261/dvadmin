# Generated by Django 3.2.3 on 2021-11-04 16:25

from django.db import migrations, models
import plugins.dvadmin_mqtt_iot.models


class Migration(migrations.Migration):

    dependencies = [
        ('dvadmin_mqtt_iot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ackmodel',
            name='metadata',
            field=models.JSONField(default=plugins.dvadmin_mqtt_iot.models.defaultDict),
        ),
        migrations.AlterField(
            model_name='connectmodel',
            name='conn_props',
            field=models.JSONField(default=plugins.dvadmin_mqtt_iot.models.defaultDict),
        ),
        migrations.AlterField(
            model_name='connectmodel',
            name='metadata',
            field=models.JSONField(default=plugins.dvadmin_mqtt_iot.models.defaultDict),
        ),
        migrations.AlterField(
            model_name='delivermodel',
            name='flags',
            field=models.JSONField(default=plugins.dvadmin_mqtt_iot.models.defaultDict),
        ),
        migrations.AlterField(
            model_name='delivermodel',
            name='headers',
            field=models.JSONField(default=plugins.dvadmin_mqtt_iot.models.defaultDict),
        ),
        migrations.AlterField(
            model_name='delivermodel',
            name='metadata',
            field=models.JSONField(default=plugins.dvadmin_mqtt_iot.models.defaultDict),
        ),
        migrations.AlterField(
            model_name='disconnectmodel',
            name='disconn_props',
            field=models.JSONField(default=plugins.dvadmin_mqtt_iot.models.defaultDict),
        ),
        migrations.AlterField(
            model_name='disconnectmodel',
            name='metadata',
            field=models.JSONField(default=plugins.dvadmin_mqtt_iot.models.defaultDict),
        ),
        migrations.AlterField(
            model_name='subscribemodel',
            name='metadata',
            field=models.JSONField(default=plugins.dvadmin_mqtt_iot.models.defaultDict),
        ),
        migrations.AlterField(
            model_name='unsubscribemodel',
            name='metadata',
            field=models.JSONField(default=plugins.dvadmin_mqtt_iot.models.defaultDict),
        ),
    ]
