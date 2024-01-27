from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.shared.models import BaseModel


class Product(BaseModel):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"))
    brand = models.ForeignKey("product.Brand", verbose_name=_("brand"), on_delete=models.CASCADE)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self) -> str:
        return self.name
