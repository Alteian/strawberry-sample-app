import os
from datetime import timedelta

from decouple import AutoConfig
from django.db import models
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet

from .base import *  # noqa: F403

for cls in [QuerySet, BaseManager, models.ForeignKey, models.ManyToManyField]:
    if not hasattr(cls, "__class_getitem__"):
        cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)  # type: ignore


config = AutoConfig(os.environ.get("DJANGO_CONFIG_ENV_DIR"))

ALLOWED_HOSTS.append("localhost")  # noqa: F405

DEBUG = config("DEBUG", cast=bool, default=False)
SECRET_KEY = config("SECRET_KEY", cast=str, default="secret-key")

if config("DJANGO_EXTENSIONS", cast=bool, default=False):
    INSTALLED_APPS.append("django_extensions")  # noqa: F405

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

COOKIE_DOMAIN = config("COOKIE_DOMAIN", cast=str, default="localhost")
GRAPHIQL_ENABLED = config("GRAPHIQL_ENABLED", cast=bool, default=False)

AUTH_TOKEN_EXPIRATION_DELTA = timedelta(seconds=3600).total_seconds()
REFRESH_TOKEN_EXPIRATION_DELTA = timedelta(days=7).total_seconds()
