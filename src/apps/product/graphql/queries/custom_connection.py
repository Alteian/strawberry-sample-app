from collections.abc import Iterable

import strawberry
import strawberry_django
from strawberry.types import Info
from strawberry_django.filters import apply as apply_filters
from strawberry_django.optimizer import optimize
from strawberry_django.ordering import apply as apply_ordering
from strawberry_django.relay import ListConnectionWithTotalCount

import src.apps.product.graphql.filters as gql_filters
import src.apps.product.graphql.orders as gql_orders
import src.apps.product.graphql.types as gql_types
from src.apps.product.models import Product
from src.graphql_core.extensions import ContextUserExtension


@strawberry.type
class CustomConnectionQuery:
    @strawberry_django.connection(
        ListConnectionWithTotalCount[gql_types.ProductType], extensions=[ContextUserExtension()]
    )
    def custom_product_connection(
        self,
        info: Info,
        filters: gql_filters.ProductFilter | None = None,
        order: gql_orders.ProductOrder | None = None,
    ) -> Iterable[gql_types.ProductType]:
        qs = optimize(gql_types.ProductType.get_queryset(Product.objects.all(), info), info)
        if filters:
            qs = apply_filters(filters, qs)
        if order:
            qs = apply_ordering(order, qs)
        return qs
