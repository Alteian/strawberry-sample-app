import strawberry
import strawberry_django
from strawberry_django.relay import ListConnectionWithTotalCount

import src.apps.product.graphql.types as gql_types


@strawberry.type
class GenericQuery:
    product: gql_types.ProductType = strawberry_django.node()
    product_list: ListConnectionWithTotalCount[gql_types.ProductType] = strawberry_django.field()
    product_connection: ListConnectionWithTotalCount[gql_types.ProductType] = strawberry_django.connection()
