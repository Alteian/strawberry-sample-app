from typing import Annotated

import strawberry


@strawberry.type
class RegisterSuccess:
    message: str


@strawberry.type
class RegisterError:
    message: str


RegisterPayload = Annotated[RegisterSuccess | RegisterError, strawberry.union(name="RegisterPayload")]

__all__ = [
    "RegisterSuccess",
    "RegisterError",
    "RegisterPayload",
]
