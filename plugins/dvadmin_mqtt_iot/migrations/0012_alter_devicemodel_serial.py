# Generated by Django 3.2.3 on 2021-11-11 08:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dvadmin_mqtt_iot', '0011_auto_20211109_0254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicemodel',
            name='serial',
            field=models.CharField(default=uuid.UUID('5bdbe0fc-ab23-47e3-82ea-26a50cdcedec'), help_text='序列号', max_length=255, verbose_name='序列号'),
        ),
    ]