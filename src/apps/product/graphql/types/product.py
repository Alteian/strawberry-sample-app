from typing import TYPE_CHECKING, Annotated, Any

import strawberry
import strawberry_django
from django.db.models import QuerySet
from strawberry.types import Info

from src.apps.product.graphql.filters import ProductFilter
from src.apps.product.graphql.orders import ProductOrder
from src.apps.product.models import Product

if TYPE_CHECKING:
    from src.apps.product.graphql.types import BrandType, ProductImageType


@strawberry_django.type(model=Product, name="Product", filters=ProductFilter, order=ProductOrder)
class ProductType(strawberry.relay.Node):
    name: strawberry.auto
    brand: Annotated["BrandType", strawberry.lazy("src.apps.product.graphql.types")] | None
    images: list[Annotated["ProductImageType", strawberry.lazy("src.apps.product.graphql.types")]]

    @classmethod
    def get_queryset(cls, queryset: QuerySet[Product], info: Info, **kwargs: Any) -> QuerySet[Product]:
        """
        Custom filtering logic for the ProductType.

        Exempli gratia visibility filter based on context user.
        """
        return queryset
