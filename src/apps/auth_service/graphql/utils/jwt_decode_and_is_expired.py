import time
from typing import Any

import jwt

from src.apps.auth_service.graphql.exceptions import TokenExpiredException
from src.apps.auth_service.utils import public_key


def jwt_decode_and_is_expired(token: str) -> Any:
    """
    Pass encoded token to receive decoded token and verify expiration.
    """
    # with options verify_exp=True, we get generic error message "Signature has expired"
    key = public_key()
    jwt_token = jwt.decode(token, key=key, algorithms=["EdDSA"], options={"verify_exp": False})
    if jwt_token["exp"] <= int(time.time()):
        raise TokenExpiredException("Token expired.")
    elif jwt_token["exp"] > int(time.time()):
        return jwt_token
