from django.db import models

from src.apps.shared.models import BaseUserModel
from src.apps.user.choices import UserRoleChoices
from src.apps.user.managers import UserManager


class User(BaseUserModel):
    objects = UserManager()

    USERNAME_FIELD = EMAIL_FIELD = "email"

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=320, unique=True)
    password = models.CharField(max_length=255)
    role = models.PositiveSmallIntegerField(choices=UserRoleChoices.choices, default=UserRoleChoices.USER)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "user"
