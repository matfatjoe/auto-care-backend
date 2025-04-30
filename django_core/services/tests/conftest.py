import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from authentication.models import Profile
from services.models import Service
from products.models import Product


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
def create_service(db):
    """Creates a service associated with a profile."""
    def _create_service(profile=None):
        if profile is None:
            profile = create_profile(db=db)
        return Service.objects.create(
            user=profile,
            name="Interior Cleaning",
            description="Full interior clean",
            pricing_type=Service.PRINCING_TYPE_FIXED,
            base_price=150.00,
            estimated_time=90
        )
    return _create_service


@pytest.fixture
def create_product(db: None):
    """Creates a product associated with a profile."""
    def _create_product(profile=None):
        if profile is None:
            profile = create_profile(db=db)
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
    return _create_product
