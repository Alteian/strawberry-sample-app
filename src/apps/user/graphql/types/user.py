import uuid

import strawberry
import strawberry_django

from src.apps.user.choices import UserRoleChoices
from src.apps.user.models import User


@strawberry_django.type(User)
class UserType(strawberry.relay.Node):
    id: strawberry.relay.NodeID[uuid.UUID]
    first_name: strawberry.auto
    last_name: strawberry.auto
    email: strawberry.auto
    is_active: strawberry.auto
    role: UserRoleChoices
    is_verified: strawberry.auto
