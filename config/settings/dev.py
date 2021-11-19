from .base import *  # noqa
from .base import env

# GENERAL
DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="RwAbLJuwWo3q7gAZjIsWq9RRQRbeJWFEgAyNZuvskVYDLvxLNQw97EDUVcq6gUYj",
)


# MIDDLEWARE.insert(-1,"utils.middlewares.visitor.VisitMiddleware")
