import uuid

from pydantic import BaseModel


class AuthToken(BaseModel):
    id: uuid.UUID
    iat: int
    exp: int
