import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def _create_user(username="johndoe", email="john@example.com", password="secret123", is_active=True):
        return User.objects.create_user(username=username, email=email, password=password, is_active=is_active)
    return _create_user
