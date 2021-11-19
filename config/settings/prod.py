from .base import *
from .base import env

# GENERAL
SECRET_KEY = env("DJANGO_SECRET_KEY",None)
assert SECRET_KEY is not None, '生产环境，请设置SECRET_KEY'



# DATABASES
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# MIDDLEWARE.insert(-1,"utils.middlewares.visitor.VisitMiddleware")
