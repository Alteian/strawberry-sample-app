import strawberry
from django.utils.translation import gettext_lazy as _
from strawberry.types import Info

import src.apps.user.graphql.responses as responses


@strawberry.type
class ContextUserQuery:
    @strawberry.field
    async def context_user(self, info: Info) -> responses.ContextUserResponse:
        user = await info.context.user
        if user.is_anonymous:
            return responses.ContextUserError(message=str(_("User is not authenticated")))
        return responses.ContextUserSuccess(user=user)
