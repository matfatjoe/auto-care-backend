from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    """
    Model to store user profile information.
    """
    user = models.OneToOneField(User, primary_key=True,
                                on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
