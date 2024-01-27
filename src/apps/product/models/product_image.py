from uuid import UUID

from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.product.models.product import Product
from src.apps.shared.models import BaseModel


class ProductImage(BaseModel):
    """
    Product image model.
    """

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    product_id: UUID
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name="images",
        db_index=True,
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        max_length=2000,
    )
