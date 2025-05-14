import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from authentication.models import Profile
from clients.models import Client


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

    def _create_profile(user=None, full_name="John Doe", username="john_doe"):
        if user is None:
            user = create_user(username=username)
        return Profile.objects.create(
            user=user, full_name=full_name, phone="1234567890"
        )

    return _create_profile


@pytest.fixture
def create_client(create_profile):
    """Creates a client associated with a user."""

    def _create_client(profile=None):
        if profile is None:
            profile = create_profile()
        return Client.objects.create(
            user=profile,
            full_name="John Doe",
            phone="1111111111",
            email="johndoe@example.com",
        )

    return _create_client
