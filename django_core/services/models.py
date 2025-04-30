from django.db import models
from uuid import uuid4
from django.core.exceptions import ValidationError


class Service(models.Model):
    PRICING_TYPE_FIXED = 'fixed'
    PRICING_TYPE_HOURLY = 'hourly'
    PRICING_TYPE_BONUS = 'bonus'
    PRICING_TYPE_CHOICES = [
        (PRICING_TYPE_FIXED, 'Fixed'),
        (PRICING_TYPE_HOURLY, 'Hourly'),
        (PRICING_TYPE_BONUS, 'Bonus')
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey('authentication.Profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    pricing_type = models.CharField(
        max_length=50,
        choices=PRICING_TYPE_CHOICES
    )
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_time = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.name is None or self.name.strip() == "":
            raise ValidationError("Name cannot be null or empty.")
        if self.description is None or self.description.strip() == "":
            raise ValidationError("Description cannot be null or empty.")
        if self.pricing_type not in dict(self.PRICING_TYPE_CHOICES):
            raise ValidationError("Invalid pricing type.")
        if self.base_price is None or self.base_price < 0:
            raise ValidationError("Base price cannot be null or negative.")
        if self.estimated_time is None or self.estimated_time < 0:
            raise ValidationError("Estimated time cannot be null or negative.")


class ServiceProduct(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def clean(self):
        if self.service is None:
            raise ValidationError("Service cannot be null.")
        if self .product is None:
            raise ValidationError("Product cannot be null.")
        if self.quantity is None or self.quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")
