import strawberry
import strawberry_django

from src.apps.product.models import Brand


@strawberry_django.filter(Brand, lookups=True)
class BrandFilter:
    name: strawberry.auto
