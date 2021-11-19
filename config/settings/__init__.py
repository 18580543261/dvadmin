from .base import env


isdev = env.bool("DJANGO_DEV", default=False)

if isdev:
    print('开发环境，使用dev配置')
    from .dev import *
else:
    print('生产环境，使用prod配置')
    from .prod import *


from plugins import *

print('settings:SHARED_APPS',SHARED_APPS)
print('settings:TENANT_APPS',TENANT_APPS)
print('settings:INSTALLED_APPS',INSTALLED_APPS)