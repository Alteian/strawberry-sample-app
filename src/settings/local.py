import os
from datetime import timedelta

from decouple import AutoConfig

from .base import *  # noqa: F403

config = AutoConfig(os.environ.get("DJANGO_CONFIG_ENV_DIR"))

ALLOWED_HOSTS.append("localhost")  # noqa: F405

DEBUG = config("DEBUG", cast=bool, default=False)
SECRET_KEY = config("SECRET_KEY")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("POSTGRES_DATABASE", default="postgres"),
        "USER": config("POSTGRES_USER", default="postgres"),
        "HOST": config("POSTGRES_HOST", default="localhost"),
        "PORT": config("POSTGRES_PORT", default="5432"),
        "PASSWORD": config("POSTGRES_PASSWORD", default="postgres"),
        "CONN_MAX_AGE": 600,
    }
}

COOKIE_DOMAIN = config("COOKIE_DOMAIN", cast=str, default="localhost")
GRAPHIQL_ENABLED = config("GRAPHIQL_ENABLED", cast=bool, default=False)

AUTH_TOKEN_EXPIRATION_DELTA = timedelta(seconds=3600).total_seconds()
REFRESH_TOKEN_EXPIRATION_DELTA = timedelta(days=7).total_seconds()
if DEBUG:
    import socket

    DEV_APPS = ["django_extensions", "debug_toolbar"]
    INSTALLED_APPS.extend(DEV_APPS)  # noqa: F405
    MIDDLEWARE.insert(0, "strawberry_django.middlewares.debug_toolbar.DebugToolbarMiddleware")  # noqa: F405
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
