from typing import Annotated

import strawberry


@strawberry.type
class LoginSuccess:
    message: str
    access_token: str


@strawberry.type
class LoginError:
    message: str


LoginPayload = Annotated[LoginSuccess | LoginError, strawberry.union(name="LoginPayload")]

__all__ = [
    "LoginSuccess",
    "LoginError",
    "LoginPayload",
]
