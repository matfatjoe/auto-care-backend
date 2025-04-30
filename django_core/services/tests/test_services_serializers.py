from rest_framework import serializers
import pytest
from uuid import UUID
from services.serializers import ServiceSerializer
from services.models import Service, ServiceProduct


@pytest.mark.django_db
class TestServiceSerializer:
    def test_valid_data_creates_service(self, create_profile, create_product):
        profile = create_profile()
        product = create_product(profile)

        data = {
            "name": "Interior Cleaning",
            "description": "Full interior clean",
            "pricing_type": Service.PRICING_TYPE_FIXED,
            "base_price": "150.00",
            "estimated_time": 90,
            "products": [
                {"product": str(product.id), "quantity": "2.5"},
            ],
        }

        request_mock = type("Request", (), {"user": profile})()
        serializer = ServiceSerializer(data=data, context={"request": request_mock})

        assert serializer.is_valid(), serializer.errors
        service = serializer.save()

        assert service.name == data["name"]
        assert service.user_id == profile.user.id

        service_product = ServiceProduct.objects.get(service=service, product=product)
        assert service_product.quantity == 2.5
        assert service_product.user_id == profile.user.id

    def test_missing_required_fields_should_fail(self, create_profile):
        profile = create_profile()
        data = {
            "description": "Full interior clean",
            "pricing_type": Service.PRICING_TYPE_FIXED,
        }

        request_mock = type("Request", (), {"user": profile})()
        serializer = ServiceSerializer(data=data, context={"request": request_mock})

        assert not serializer.is_valid()
        assert "name" in serializer.errors
        assert "base_price" in serializer.errors
        assert "estimated_time" in serializer.errors

    @pytest.mark.parametrize(
        "pricing_type, is_valid",
        [
            (Service.PRICING_TYPE_FIXED, True),
            (Service.PRICING_TYPE_HOURLY, True),
            (Service.PRICING_TYPE_BONUS, True),
            ("invalid_type", False),
            (None, False),
        ],
    )
    def test_pricing_type_validation(self, create_profile, pricing_type, is_valid):
        profile = create_profile()
        data = {
            "name": "Test Service",
            "description": "Testing pricing type",
            "pricing_type": pricing_type,
            "base_price": "50.00",
            "estimated_time": 60,
        }

        request_mock = type("Request", (), {"user": profile})()
        serializer = ServiceSerializer(data=data, context={"request": request_mock})

        if is_valid:
            assert serializer.is_valid(), serializer.errors
        else:
            assert not serializer.is_valid()
            assert "pricing_type" in serializer.errors

    def test_negative_price_should_fail(self, create_profile):
        profile = create_profile()
        data = {
            "name": "Quick Wash",
            "description": "Basic wash",
            "pricing_type": Service.PRICING_TYPE_FIXED,
            "base_price": "-10.00",
            "estimated_time": 30,
        }

        request_mock = type("Request", (), {"user": profile})()
        serializer = ServiceSerializer(data=data, context={"request": request_mock})

        assert not serializer.is_valid()
        assert "base_price" in serializer.errors

    def test_read_only_fields_are_ignored_on_create(self, create_profile):
        profile = create_profile()

        fake_date = "2000-01-01T00:00:00Z"
        data = {
            "id": "fake-id",
            "name": "Polishing",
            "description": "Paint polishing",
            "pricing_type": Service.PRICING_TYPE_FIXED,
            "base_price": "300.00",
            "estimated_time": 90,
            "created_at": fake_date,
            "updated_at": fake_date,
        }

        request_mock = type("Request", (), {"user": profile})()
        serializer = ServiceSerializer(data=data, context={"request": request_mock})

        assert serializer.is_valid(), serializer.errors
        service = serializer.save()

        assert str(service.id) != "fake-id"
        assert UUID(str(service.id))
        assert service.created_at.isoformat() != fake_date
        assert service.updated_at.isoformat() != fake_date

    def test_invalid_product_id_should_fail_on_save(self, create_profile):
        profile = create_profile()

        data = {
            "name": "Engine Detailing",
            "description": "Deep clean of the engine bay",
            "pricing_type": Service.PRICING_TYPE_FIXED,
            "base_price": "200.00",
            "estimated_time": 60,
            "products": [
                {"product": "00000000-0000-0000-0000-000000000000", "quantity": "1.0"},
            ],
        }

        request_mock = type("Request", (), {"user": profile})()
        serializer = ServiceSerializer(data=data, context={"request": request_mock})

        assert serializer.is_valid(), serializer.errors

        with pytest.raises(serializers.ValidationError) as error:
            serializer.save()

        print(error)
        assert "message" in error.value.detail
        assert error.value.detail["message"] == "One or more products do not exist."

    @pytest.mark.parametrize("invalid_quantity", [None, "-1", "0"])
    def test_invalid_quantity_should_fail(self, create_profile, invalid_quantity):
        profile = create_profile()

        data = {
            "name": "Wheel Cleaning",
            "description": "Clean wheels thoroughly",
            "pricing_type": Service.PRICING_TYPE_FIXED,
            "base_price": "100.00",
            "estimated_time": 45,
            "products": [
                {
                    "product": "00000000-0000-0000-0000-000000000000",
                    "quantity": invalid_quantity,
                },
            ],
        }

        request_mock = type("Request", (), {"user": profile})()
        serializer = ServiceSerializer(data=data, context={"request": request_mock})
        assert not serializer.is_valid()
        assert "products" in serializer.errors
        assert "Quantity must be greater than 0." in str(serializer.errors["products"])
