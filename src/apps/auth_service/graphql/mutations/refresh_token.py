import time
from calendar import timegm

import jwt
import strawberry
from asgiref.sync import sync_to_async
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from strawberry.types import Info

import src.apps.auth_service.graphql.exceptions as exceptions
import src.apps.auth_service.graphql.payloads as payloads
from src.apps.auth_service.models import AuthToken, RefreshToken
from src.apps.auth_service.utils import private_key
from src.apps.shared.utils import UUIDEncoder


@strawberry.type
class RefreshTokenMutation:
    @strawberry.mutation
    @sync_to_async
    def refresh_token(self, info: Info) -> payloads.RefreshTokenPayload:
        try:
            refresh_token = RefreshToken.objects.get(token=info.context["request"].COOKIES.get("refresh_token"))
            if refresh_token.is_expired():
                raise exceptions.RefreshTokenExpiredException
            refresh_token.reuse()
            refresh_token.token = refresh_token.generate_token()
            refresh_token.save()
            orig_iat = timegm(refresh_token.created_at.timetuple())
            exp = orig_iat + settings.REFRESH_TOKEN_EXPIRATION_DELTA
            info.context["response"].set_cookie(
                key="refresh_token",
                value=refresh_token.token,
                domain=settings.COOKIE_DOMAIN,
                max_age=exp,
                httponly=True,
                secure=True,
                samesite="None",
            )
            epoch_time = int(time.time())
            encoded_payload = jwt.encode(
                payload=AuthToken(
                    id=refresh_token.user.id,
                    iat=epoch_time,
                    exp=epoch_time + settings.AUTH_TOKEN_EXPIRATION_DELTA,
                ).model_dump(),
                key=private_key(),
                algorithm="EdDSA",
                json_encoder=UUIDEncoder,
            )
            return payloads.RefreshTokenSuccess(
                message=str(_("Enjoy more time which you've been granted")),
                access_token=encoded_payload,
            )
        except exceptions.RefreshTokenExpiredException:
            refresh_token.delete()
            return payloads.RefreshTokenError(message=str(_("Log in again")))
        except RefreshToken.DoesNotExist:
            return payloads.RefreshTokenError(message=str(_("Invalid refresh token")))
        except Exception as error:
            return payloads.RefreshTokenError(message=str(error))
