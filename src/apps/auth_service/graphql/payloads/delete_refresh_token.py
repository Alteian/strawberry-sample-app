from typing import Annotated

import strawberry


@strawberry.type
class DeleteCookieTokenSuccess:
    message: str


@strawberry.type
class DeleteCookieTokenError:
    message: str


DeleteCookieTokenPayload = Annotated[
    DeleteCookieTokenSuccess | DeleteCookieTokenError, strawberry.union(name="DeleteCookieTokenPayload")
]

__all__ = [
    "DeleteCookieTokenSuccess",
    "DeleteCookieTokenError",
    "DeleteCookieTokenPayload",
]
