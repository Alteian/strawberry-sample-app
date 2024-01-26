from pathlib import Path

from django.conf import settings
from strawberry import Schema
from strawberry.extensions import QueryDepthLimiter
from strawberry.schema.config import StrawberryConfig
from strawberry_django.optimizer import DjangoOptimizerExtension

from src.apps.auth_service.graphql.mutations import AuthServiceMutation
from src.apps.user.graphql.queries import UserQuery

Mutation = AuthServiceMutation


schema_extensions = [
    QueryDepthLimiter(max_depth=10),  # TODO: find optimal amount.
    DjangoOptimizerExtension,
]
pyinstrument_path = Path(settings.BASE_DIR) / "pyinstrument.html"
if settings.DEBUG:
    from strawberry.extensions import pyinstrument

    schema_extensions.append(pyinstrument.PyInstrument(report_path=pyinstrument_path))


Query = UserQuery

schema = Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(
        auto_camel_case=True,
    ),
    extensions=schema_extensions,
)
