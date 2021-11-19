from django.apps import AppConfig


class DvadminApschedulerBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.dvadmin_mqtt_iot'
    url_prefix = "dvadmin_mqtt_iot",
