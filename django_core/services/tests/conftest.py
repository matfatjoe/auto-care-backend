import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from authentication.models import Profile


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def create_user(db):
    """Creates a user."""
    def _create_user(username: str = "john_doe", password: str = "password123"):
        return User.objects.create_user(username=username, password=password)
    return _create_user


@pytest.fixture
def create_profile(db, create_user):
    """Creates a profile associated with a user."""
    def _create_profile(user=None):
        if user is None:
            user = create_user()
        return Profile.objects.create(
            user=user,
            full_name="John Doe",
            phone="1234567890"
        )
    return _create_profile
