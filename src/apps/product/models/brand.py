from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.shared.models import BaseModel


class Brand(BaseModel):
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("brand")
        verbose_name_plural = _("brands")

    def __str__(self) -> str:
        return self.name
