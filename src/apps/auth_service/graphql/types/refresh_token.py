import uuid

import strawberry
import strawberry_django
from strawberry.relay import NodeID

from src.apps.auth_service.models import RefreshToken


@strawberry_django.type(RefreshToken)
class RefreshTokenType:
    id: NodeID[uuid.UUID]
    user: strawberry.auto
    token: strawberry.auto
    created_at: strawberry.auto
