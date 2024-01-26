from strawberry.tools import merge_types

from .context_user import ContextUserQuery
from .generic import GenericQuery

UserQuery = merge_types(name="UserQuery", types=(GenericQuery, ContextUserQuery))
