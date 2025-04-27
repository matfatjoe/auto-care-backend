import uuid
from django.db import models
from django.core.exceptions import ValidationError

from authentication.models import Profile


class Product(models.Model):
    UNIT_TYPE_ML = 'ml'
    UNIT_TYPE_UNIT = 'unit'
    UNIT_TYPE_CHOICES = [
        (UNIT_TYPE_ML, 'Milliliters'),
        (UNIT_TYPE_UNIT, 'Unit')
    ]

    PRODUCT_TYPE_SUPPLY = 'supply'
    PRODUCT_TYPE_ACCESSORY = 'accessory'
    PRODUCT_TYPE_CHOICES = [
        (PRODUCT_TYPE_SUPPLY, 'Supply'),
        (PRODUCT_TYPE_ACCESSORY, 'Accessory')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    unit_type = models.CharField(
        max_length=50,
        choices=UNIT_TYPE_CHOICES
    )
    product_type = models.CharField(
        max_length=50,
        choices=PRODUCT_TYPE_CHOICES
    )
    last_purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    stock_control_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.unit_type not in dict(self.UNIT_TYPE_CHOICES):
            raise ValidationError(f"Invalid unit type: {self.unit_type}")

        if self.product_type not in dict(self.PRODUCT_TYPE_CHOICES):
            raise ValidationError(f"Invalid product type: {self.product_type}")

        if self.last_purchase_price is not None and self.last_purchase_price < 0:
            raise ValidationError("Last purchase price cannot be negative.")

        if self.sale_price is not None and self.sale_price < 0:
            raise ValidationError("Sale price cannot be negative.")

        if self.stock_quantity is not None and self.stock_quantity < 0:
            raise ValidationError("Stock quantity cannot be negative.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
