import strawberry
import strawberry_django
from asgiref.sync import sync_to_async

from src.apps.product.models import ProductImage


@strawberry_django.type(model=ProductImage, name="ProductImage")
class ProductImageType(strawberry.relay.Node):
    @strawberry_django.field(only=["image"])
    @sync_to_async
    def image(self, root: ProductImage) -> str | None:
        return root.image.url if root.image else None
