import pytest
from services.serializers import ServiceSerializer
from services.models import Service


@pytest.mark.django_db
class TestServiceSerializer:

    def test_valid_data_creates_service(self, create_profile):
        profile = create_profile()
        data = {
            "user": profile.user.id,
            "name": "Interior Cleaning",
            "description": "Full interior clean",
            "pricing_type": Service.PRICING_TYPE_FIXED,
            "base_price": "150.00",
            "estimated_time": 90,
        }

        serializer = ServiceSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        service = serializer.save(profile=profile)

        assert service.name == data["name"]
#     def test_missing_required_fields_should_fail(self):
#         data = {
#             "user": self.profile.id,
#             "description": "Faltando nome",
#             "pricing_type": Service.PRICING_TYPE_FIXED,
#         }

#         serializer = ServiceSerializer(data=data)
#         assert not serializer.is_valid()
#         assert "name" in serializer.errors
#         assert "base_price" in serializer.errors
#         assert "estimated_time" in serializer.errors

#     def test_invalid_pricing_type_should_fail(self):
#         data = {
#             "user": self.profile.id,
#             "name": "Lavagem X",
#             "description": "Teste",
#             "pricing_type": "invalid_type",
#             "base_price": "50.00",
#             "estimated_time": 60,
#         }

#         serializer = ServiceSerializer(data=data)
#         assert not serializer.is_valid()
#         assert "pricing_type" in serializer.errors


# @pytest.mark.django_db
# class TestServiceProductUsageSerializer:
#     def setup_method(self):
#         self.profile = self.create_profile()
#         self.service = Service.objects.create(
#             user=self.profile,
#             name="Lavagem Simples",
#             pricing_type=Service.PRICING_TYPE_FIXED,
#             base_price=100,
#             estimated_time=60,
#         )
#         self.product = Product.objects.create(
#             user=self.profile,
#             name="Shampoo",
#             unit_type=Product.UNIT_TYPE_ML,
#             product_type=Product.PRODUCT_TYPE_SUPPLY,
#             last_purchase_price=20,
#             sale_price=30,
#             stock_quantity=100,
#             stock_control_enabled=True,
#         )

#     def create_profile(self):
#         from profiles.models import Profile
#         return Profile.objects.create_user(
#             username="testuser2", email="test2@example.com", password="testpass"
#         ).profile

#     def test_valid_service_product_data(self):
#         data = {
#             "service": self.service.id,
#             "product": self.product.id,
#             "quantity": "50.00",
#         }

#         serializer = ServiceProductUsageSerializer(data=data)
#         assert serializer.is_valid(), serializer.errors
#         usage = serializer.save()

#         assert usage.service_id == self.service.id
#         assert usage.product_id == self.product.id
#         assert usage.quantity == 50

#     def test_invalid_quantity_should_fail(self):
#         data = {
#             "service": self.service.id,
#             "product": self.product.id,
#             "quantity": "-10.00",
#         }

#         serializer = ServiceProductUsageSerializer(data=data)
#         assert not serializer.is_valid()
#         assert "quantity" in serializer.errors

#     def test_missing_fields_should_fail(self):
#         data = {"quantity": "30.00"}  # missing product and service

#         serializer = ServiceProductUsageSerializer(data=data)
#         assert not serializer.is_valid()
#         assert "service" in serializer.errors
#         assert "product" in serializer.errors
