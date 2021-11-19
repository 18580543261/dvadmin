from django.apps import AppConfig


class DvadminApschedulerBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.wxlogin'
    url_prefix = "wxlogin",
