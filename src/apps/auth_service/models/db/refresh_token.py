import binascii
import os
import uuid
from calendar import timegm
from datetime import datetime, timedelta
from typing import Any

from django.conf import settings
from django.db import models
from django.db.models import Case, Value, When
from django.dispatch import Signal
from django.utils import timezone

refresh_token_rotated = Signal()


def refresh_has_expired(orig_iat: int) -> bool:
    exp = orig_iat + timedelta(days=7).total_seconds()
    return timegm(datetime.utcnow().utctimetuple()) > exp


class RefreshTokenQuerySet(models.QuerySet):
    def expired(self: models.QuerySet["RefreshToken"]) -> models.QuerySet:
        expires = timezone.now() - timedelta(days=7)
        return self.annotate(
            expired=Case(
                When(created_at__lt=expires, then=Value(True)),
                output_field=models.BooleanField(),
                default=Value(False),
            ),
        )


class AbstractRefreshToken(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="refresh_tokens",
        verbose_name="user",
    )
    token = models.CharField(max_length=255, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = RefreshTokenQuerySet.as_manager()

    class Meta:
        abstract = True
        verbose_name = "refresh token"
        verbose_name_plural = "refresh tokens"
        unique_together = ("token", "user")

    def __str__(self):
        return self.token

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.token:
            self.token = self._cached_token = self.generate_token()

        super().save(*args, **kwargs)

    def generate_token(self) -> str:
        return binascii.hexlify(
            os.urandom(20),
        ).decode()

    def get_token(self) -> str:
        if hasattr(self, "_cached_token"):
            return self._cached_token
        return self.token

    def is_expired(self) -> bool:
        orig_iat = timegm(self.created_at.timetuple())
        return refresh_has_expired(orig_iat)

    def reuse(self) -> None:
        self.token = ""  # nosec B105
        self.created_at = timezone.now()
        self.save(update_fields=["token", "created_at"])


class RefreshToken(AbstractRefreshToken):
    """
    RefreshToken default model.
    """
