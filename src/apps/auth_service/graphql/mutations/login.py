import time
from calendar import timegm

import jwt
import strawberry
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from strawberry.types import Info

import src.apps.auth_service.graphql.payloads as payloads
from src.apps.auth_service.graphql.exceptions import (
    CredentialsException,
    UserIsNotVerifiedException,
)
from src.apps.auth_service.graphql.inputs import LoginInput
from src.apps.auth_service.models import AuthToken, RefreshToken
from src.apps.auth_service.utils import private_key
from src.apps.shared.utils import UUIDEncoder


@strawberry.type
class LoginMutation:
    @strawberry.mutation
    @sync_to_async
    def login(self, info: Info, input: LoginInput) -> payloads.LoginPayload:
        try:
            user = get_user_model().objects.get(email=input.email)
            if not user.check_password(input.password):
                raise CredentialsException
            if not user.is_verified:
                raise UserIsNotVerifiedException
            epoch_time = int(time.time())
            encoded_payload = jwt.encode(
                payload=AuthToken(
                    id=user.id,
                    iat=epoch_time,
                    exp=epoch_time + settings.AUTH_TOKEN_EXPIRATION_DELTA,
                ).model_dump(),
                key=private_key(),
                algorithm="EdDSA",
                json_encoder=UUIDEncoder,
            )
            refresh_token, placeholder = RefreshToken.objects.get_or_create(user=user)
            # Not sure how to handle expired tokens yet #####
            if refresh_token.is_expired():
                refresh_token.delete()
                refresh_token = RefreshToken.objects.create(user=user)
            #####################################################
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
            user.last_login = timezone.now()
            user.save()
            return payloads.LoginSuccess(
                message=str(_("Successfully logged in")),
                access_token=encoded_payload,
            )
        except get_user_model().DoesNotExist:
            return payloads.LoginError(message=str(_("User with this email does not exist, please register")))
        except CredentialsException:
            return payloads.LoginError(message=str(_("Provide valid credentials")))
        except UserIsNotVerifiedException:
            return payloads.LoginError(message=str(_("Verify your account before logging in")))
