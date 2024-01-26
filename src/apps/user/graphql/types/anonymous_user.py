import strawberry

from src.apps.user.choices import UserRoleChoices


@strawberry.type
class CustomAnonymousUserType:
    is_anonymous: bool
    role: UserRoleChoices
