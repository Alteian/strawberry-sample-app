from strawberry.tools import merge_types

from .delete_refresh_token import DeleteCookieTokenMutation
from .login import LoginMutation
from .refresh_token import RefreshTokenMutation
from .register import RegisterMutation
from .verify_user import VerifyUserMutation

AuthServiceMutation = merge_types(
    name="AuthServiceMutation",
    types=(
        LoginMutation,
        DeleteCookieTokenMutation,
        RefreshTokenMutation,
        RegisterMutation,
        VerifyUserMutation,
    ),
)
