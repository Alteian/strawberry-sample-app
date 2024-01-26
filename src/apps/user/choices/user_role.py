import strawberry
from django.db import models


@strawberry.enum
class UserRoleChoices(models.IntegerChoices):
    USER = 1, "User"
    ANONYMOUS = 2, "Anonymous"
