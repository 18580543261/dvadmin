from django.apps import AppConfig


class DvadminApschedulerBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins.user'
    url_prefix = "user",
