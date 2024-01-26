from typing import Annotated

import strawberry


@strawberry.type
class VerifyUserSuccess:
    message: str


@strawberry.type
class VerifyUserError:
    message: str


VerifyUserPayload = Annotated[VerifyUserSuccess | VerifyUserError, strawberry.type(name="VerifyUserPayload")]

__all__ = [
    "VerifyUserSuccess",
    "VerifyUserError",
    "VerifyUserPayload",
]
