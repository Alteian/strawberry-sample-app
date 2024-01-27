import strawberry
import strawberry_django

from src.apps.product.graphql.filters.brand import BrandFilter
from src.apps.product.models import Brand


@strawberry_django.type(
    Brand,
    name="Brand",
    filters=BrandFilter,
)
class BrandType(strawberry.relay.Node):
    name: strawberry.auto
