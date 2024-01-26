import strawberry
from asgiref.sync import sync_to_async
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from strawberry.types import Info

import src.apps.auth_service.graphql.payloads as payloads
from src.apps.auth_service.models import RefreshToken


@strawberry.type
class DeleteCookieTokenMutation:
    @strawberry.mutation
    @sync_to_async
    def delete_cookie_token(self, info: Info) -> payloads.DeleteCookieTokenPayload:
        try:
            refresh_token = info.context["request"].COOKIES.get("refresh_token")
            RefreshToken.objects.get(token=refresh_token).delete()
            info.context["response"].delete_cookie(key="refresh_token", domain=settings.COOKIE_DOMAIN)
            return payloads.DeleteCookieTokenSuccess(message=str(_("Successfully logged out")))
        except RefreshToken.DoesNotExist:
            return payloads.DeleteCookieTokenError(message=str(_("Invalid refresh token")))
        except Exception as error:
            return payloads.DeleteCookieTokenError(message=str(error))
