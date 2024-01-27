import strawberry
import strawberry_django

from src.apps.product.models import Brand


@strawberry_django.order(Brand)
class BrandOrder:
    name: strawberry.auto
