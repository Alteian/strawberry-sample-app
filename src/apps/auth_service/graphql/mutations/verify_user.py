import strawberry
from asgiref.sync import sync_to_async
from django.utils.translation import gettext_lazy as _
from strawberry.types import Info

import src.apps.auth_service.graphql.payloads as payloads
from src.apps.auth_service.graphql.inputs import VerifyUserInput
from src.apps.user.models import User


def verify_user_fn(verification_token: str) -> int:
    user = User.objects.filter(id=verification_token).update(is_verified=True)
    return user


@strawberry.type
class VerifyUserMutation:
    @strawberry.mutation(
        description="Doesn't handle multiple verifications for same user, but let's be honest, it's not needed."
    )
    async def verify_user(
        self,
        info: Info,
        input: VerifyUserInput,
    ) -> payloads.VerifyUserPayload:
        user = await sync_to_async(verify_user_fn, thread_sensitive=True)(input.verification_token)
        if user:
            return payloads.VerifyUserSuccess(message=str(_("User verified successfully")))
        return payloads.VerifyUserError(message=str(_("User not found")))
