import strawberry
import strawberry_django

from src.apps.product.graphql.filters import ProductFilter
from src.apps.product.graphql.types import ProductType
from src.apps.product.models import Product


@strawberry_django.partial(Product)
class ProductInputPartial(strawberry_django.NodeInput):
    name: strawberry.auto
    brand: strawberry.auto


@strawberry.type
class GenericMutation:
    update_products_in_bulk_with_filters_generic: list[ProductType] = strawberry_django.mutations.update(
        ProductInputPartial, filters=ProductFilter
    )
