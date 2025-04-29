import pytest
from django.core.exceptions import ValidationError
from services.models import Service
from products.models import Product
from authentication.models import Profile
from django.utils import timezone
from uuid import uuid4


@pytest.mark.django_db
class TestServiceModel:

    def test_create_service_successfully(self, create_profile):
        profile = create_profile()
        service = Service.objects.create(
            user=profile,
            name="Interior Cleaning",
            description="Full interior clean",
            pricing_type=Service.PRINCING_TYPE_FIXED,
            base_price=150.00,
            estimated_time=90
        )

        assert service.id is not None
        assert service.user == profile
        assert service.name == "Interior Cleaning"
        assert service.description == "Full interior clean"
        assert service.pricing_type == Service.PRINCING_TYPE_FIXED
        assert service.base_price == 150.00
        assert service.estimated_time == 90
        assert service.is_deleted is False
        assert service.created_at is not None
        assert service.updated_at is not None

    def test_cannot_create_service_without_name(self, create_profile):
        profile = create_profile()
        with pytest.raises(ValidationError):
            Service.objects.create(
                user=profile,
                name="",
                description="Full interior clean",
                pricing_type=Service.PRINCING_TYPE_FIXED,
                base_price=150.00,
                estimated_time=90
            ).full_clean()

    def test_cannot_create_service_without_description(self, create_profile):
        profile = create_profile()
        with pytest.raises(ValidationError):
            Service.objects.create(
                user=profile,
                name="Interior Cleaning",
                description="",
                pricing_type=Service.PRINCING_TYPE_FIXED,
                base_price=150.00,
                estimated_time=90
            ).full_clean()

    def test_cannot_create_service_with_invalid_pricing_type(self, create_profile):
        profile = create_profile()
        with pytest.raises(ValidationError):
            Service.objects.create(
                user=profile,
                name="Interior Cleaning",
                description="Full interior clean",
                pricing_type="invalid_type",
                base_price=150.00,
                estimated_time=90
            ).full_clean()

    def test_cannot_create_service_with_negative_base_price(self, create_profile):
        profile = create_profile()
        with pytest.raises(ValidationError):
            Service.objects.create(
                user=profile,
                name="Interior Cleaning",
                description="Full interior clean",
                pricing_type=Service.PRINCING_TYPE_FIXED,
                base_price=-150.00,
                estimated_time=90
            ).full_clean()

    def test_cannot_create_service_with_negative_estimated_time(self, create_profile):
        profile = create_profile()
        with pytest.raises(ValidationError):
            Service.objects.create(
                user=profile,
                name="Interior Cleaning",
                description="Full interior clean",
                pricing_type=Service.PRINCING_TYPE_FIXED,
                base_price=150.00,
                estimated_time=-90
            ).full_clean()
