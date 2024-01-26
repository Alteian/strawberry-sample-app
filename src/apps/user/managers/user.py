from typing import TYPE_CHECKING, Any

from django.contrib.auth.base_user import BaseUserManager

if TYPE_CHECKING:
    from src.apps.user.models import User


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        **kwargs: Any,
    ) -> "User":
        from src.apps.user.models import User

        model = User
        user: User = model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_verified=True,  # NOTE: This is a temporary solution
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
