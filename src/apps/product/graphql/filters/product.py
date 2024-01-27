import strawberry
import strawberry_django
from strawberry_django.filters import FilterLookup

from src.apps.product.graphql.filters.brand import BrandFilter
from src.apps.product.models import Product


@strawberry_django.filter(Product, lookups=True)
class ProductFilter:
    id: FilterLookup[strawberry.relay.GlobalID] | None
    name: strawberry.auto
    description: strawberry.auto
    brand: BrandFilter | None
    price: strawberry.auto
