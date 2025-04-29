import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from products.models import Product
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


@pytest.fixture
def product_supply(create_profile):
    """Creates a supply product associated with a user."""
    def _create_product_supply(profile=None):
        if profile is None:
            profile = create_profile()
        return Product.objects.create(
            user=profile,
            name="Car Shampoo",
            description="High foam automotive shampoo",
            unit_type=Product.UNIT_TYPE_ML,
            product_type=Product.PRODUCT_TYPE_SUPPLY,
            last_purchase_price=50.00,
            sale_price=80.00,
            stock_quantity=100,
            stock_control_enabled=True,
        )
    return _create_product_supply


@pytest.fixture
def product_accessory(create_profile):
    """Creates an accessory product associated with a user."""
    profile = create_profile()
    product = Product.objects.create(
        user=profile,
        name="Foam Cannon PRO with 1/4″ Quick Connector Adapter",
        description="High-quality foam cannon for car washing",
        unit_type=Product.UNIT_TYPE_UNIT,
        product_type=Product.PRODUCT_TYPE_ACCESSORY,
        last_purchase_price=20.00,
        sale_price=40.00,
        stock_quantity=150,
        stock_control_enabled=True,
    )
    return product


@pytest.fixture
def authenticated_client(api_client, create_user):
    """Creates an authenticated client with a user."""
    user = create_user(username="john_doe", password="password123")
    api_client.force_authenticate(user=user)
    return api_client, user
