"""
ASGI config for src project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from strawberry_django.routers import AuthGraphQLProtocolTypeRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings.base")

asgi_app = get_asgi_application()

from src.graphql_core.schema import schema  # noqa: E402

application = AuthGraphQLProtocolTypeRouter(
    schema,
    django_application=asgi_app,
)
