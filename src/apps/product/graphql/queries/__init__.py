from strawberry.tools import merge_types

from .custom_connection import CustomConnectionQuery
from .generic import GenericQuery

ProductQuery = merge_types(name="ProductQuery", types=(GenericQuery, CustomConnectionQuery))
