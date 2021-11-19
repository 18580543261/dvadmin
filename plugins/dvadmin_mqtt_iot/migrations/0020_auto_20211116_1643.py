# Generated by Django 3.2.3 on 2021-11-16 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dvadmin_mqtt_iot', '0019_alter_devicemodel_serial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicemodel',
            name='status',
            field=models.IntegerField(choices=[(0, '离线'), (1, '在线')], default=0, help_text='设备状态', verbose_name='设备状态'),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='type',
            field=models.IntegerField(choices=[(0, '设备'), (1, '前端')], default=0, help_text='设备类型', verbose_name='设备类型'),
        ),
    ]
