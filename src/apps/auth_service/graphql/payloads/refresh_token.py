from typing import Annotated

import strawberry


@strawberry.type
class RefreshTokenSuccess:
    message: str
    access_token: str


@strawberry.type
class RefreshTokenError:
    message: str


RefreshTokenPayload = Annotated[RefreshTokenSuccess | RefreshTokenError, strawberry.union(name="RefreshTokenPayload")]

__all__ = [
    "RefreshTokenSuccess",
    "RefreshTokenError",
    "RefreshTokenPayload",
]
