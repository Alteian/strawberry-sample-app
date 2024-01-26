from typing import Optional

import strawberry
import strawberry_django
from strawberry_django.relay import ListConnectionWithTotalCount

from src.apps.user.graphql.types import UserType


@strawberry.type
class GenericQuery:
    user: Optional[UserType] = strawberry_django.node()
    user_connection: ListConnectionWithTotalCount[UserType] = strawberry_django.connection()
