from typing import TYPE_CHECKING, Annotated

import strawberry
import strawberry_django

from src.apps.product.models import Product

if TYPE_CHECKING:
    from src.apps.product.graphql.orders import BrandOrder


@strawberry_django.order(Product)
class ProductOrder:
    name: strawberry.auto
    description: strawberry.auto
    brand: Annotated["BrandOrder", strawberry.lazy("src.apps.product.graphql.orders")] | None
    price: strawberry.auto
