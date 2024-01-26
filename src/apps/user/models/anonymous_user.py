from typing import Literal

from django.contrib.auth.models import AnonymousUser

from src.apps.user.choices import UserRoleChoices


class CustomAnonymousUser(AnonymousUser):
    @property
    def is_anonymous(self) -> Literal[True]:
        return True

    @property
    def role(self) -> UserRoleChoices:
        return UserRoleChoices.ANONYMOUS
