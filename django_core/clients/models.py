from django.db import models
from uuid import uuid4
from django.core.exceptions import ValidationError


class Client(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey('authentication.Profile', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if self.full_name is None or self.full_name.strip() == "":
            raise ValidationError("Full name is required.")
        if self.phone is None or self.phone.strip() == "":
            raise ValidationError("Phone number is required.")
        if not self.phone.isdigit():
            raise ValidationError("Phone number must be numeric.")
        if self.email is None or self.email.strip() == "":
            raise ValidationError("Email is required.")
        if self.email is None or self.email.strip() == "":
            raise ValidationError("Email is invalid.")
