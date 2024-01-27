import sys
from typing import Any

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from src.apps.product.models import Brand, Product


class Command(BaseCommand):
    help = "Dummy data using dummyjson.com"

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:
        result = requests.get("https://dummyjson.com/products?limit=100", timeout=360).json()

        for p in result["products"]:
            product = Product.objects.create(
                name=p["title"],
                description=p["description"],
                brand=Brand.objects.get_or_create(name=p["brand"])[0],
                price=p["price"],
            )

            for image in p["images"]:
                raw = requests.get(image, timeout=360).content
                parts = image.split("/")
                name = f"products/{product.pk}/{parts[-1]}"
                product.images.create(image=ContentFile(raw, name=name))

            sys.stdout.write(f"* Imported {product}\n")
