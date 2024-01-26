import strawberry

from src.apps.auth_service.models import AuthToken


@strawberry.experimental.pydantic.type(model=AuthToken, all_fields=True)
class AuthTokenType:
    pass
