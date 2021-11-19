from django.conf import settings

app = 'plugins.dvadmin_mqtt_iot'
if app not in settings.INSTALLED_APPS:
    settings.INSTALLED_APPS += [app]
if getattr(settings, 'PLUGINS_LIST', {}).get('dvadmin_tenant_backend', None):
    settings.SHARED_APPS = [
                               'plugins.dvadmin_mqtt_iot',
                           ] + list(getattr(settings, 'SHARED_APPS', []))
    settings.TENANT_APPS = [
                               'plugins.dvadmin_mqtt_iot',
                           ] + list(getattr(settings, 'TENANT_APPS', []))