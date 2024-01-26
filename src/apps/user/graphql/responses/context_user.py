from typing import Annotated

import strawberry

from src.apps.user.graphql.types import UserType


@strawberry.type
class ContextUserSuccess:
    user: UserType


@strawberry.type
class ContextUserError:
    message: str


ContextUserResponse = Annotated[ContextUserSuccess | ContextUserError, strawberry.field(description="User")]
