from pathlib import Path

from django.conf import settings
from strawberry import Schema
from strawberry.extensions import QueryDepthLimiter
from strawberry.schema.config import StrawberryConfig
from strawberry.tools import merge_types
from strawberry_django.optimizer import DjangoOptimizerExtension

from src.apps.auth_service.graphql.mutations import AuthServiceMutation
from src.apps.product.graphql.mutations import ProductMutation
from src.apps.product.graphql.queries import ProductQuery
from src.apps.user.graphql.mutations import GenericMutation
from src.apps.user.graphql.queries import UserQuery

Mutation = merge_types(
    "Mutation",
    types=(GenericMutation, AuthServiceMutation, ProductMutation),
)


schema_extensions = [
    QueryDepthLimiter(max_depth=10),  # TODO: find optimal amount.
    DjangoOptimizerExtension,
]
pyinstrument_path = Path(settings.BASE_DIR) / "pyinstrument.html"
if settings.DEBUG:
    from strawberry.extensions import pyinstrument

    schema_extensions.append(pyinstrument.PyInstrument(report_path=pyinstrument_path))


Query = merge_types(
    "Query",
    types=(UserQuery, ProductQuery),
)

schema = Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(
        auto_camel_case=True,
    ),
    extensions=schema_extensions,
)
