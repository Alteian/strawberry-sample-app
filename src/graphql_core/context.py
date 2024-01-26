from functools import cached_property
from typing import Union, cast

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from graphql.error import GraphQLError
from strawberry.django.context import StrawberryDjangoContext

from src.apps.auth_service.graphql.exceptions import TokenExpiredException
from src.apps.auth_service.graphql.utils import jwt_decode_and_is_expired
from src.apps.user.graphql.types import CustomAnonymousUserType, UserType
from src.apps.user.models import CustomAnonymousUser


class Context(StrawberryDjangoContext):
    @cached_property
    @sync_to_async
    def user(self) -> Union[UserType, CustomAnonymousUserType, None]:
        authorization = self.request.headers.get("Authorization", None)
        if not self.request:
            return None
        elif not authorization:
            # Could refresh token if present?
            return cast(CustomAnonymousUserType, CustomAnonymousUser())
        try:
            decoded = jwt_decode_and_is_expired(authorization)
            id = decoded.get("id", None)
            user = get_user_model().objects.get(id=id)
            return cast(UserType, user)
        except TokenExpiredException as e:
            raise GraphQLError(message=str(e))
        except get_user_model().DoesNotExist:
            raise GraphQLError(message=str(_("User not found")))
