import pytest
from products.serializers import ProductSerializer
from products.models import Product


@pytest.mark.django_db
class TestProductSerializer:
    def test_product_serializer_valid_data(self, create_profile):
        profile = create_profile()
        data = {
            "user": profile.user.id,
            "name": "Car Shampoo",
            "description": "High foam automotive shampoo",
            "unit_type": Product.UNIT_TYPE_ML,
            "product_type": Product.PRODUCT_TYPE_SUPPLY,
            "last_purchase_price": 50.00,
            "sale_price": 80.00,
            "stock_quantity": 100,
            "stock_control_enabled": True,
        }
        serializer = ProductSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        product = serializer.save(user=profile)
        assert product.name == "Car Shampoo"
        assert product.unit_type == "ml"
        assert product.product_type == "supply"
        assert product.last_purchase_price == 50.00
        assert product.sale_price == 80.00
        assert product.stock_quantity == 100
        assert product.stock_control_enabled is True
        assert product.user == profile

    def test_product_serializer_missing_name(self, create_profile):
        profile = create_profile()
        data = {
            "user": profile.user.id,
            "description": "High foam automotive shampoo",
            "unit_type": Product.UNIT_TYPE_ML,
            "product_type": Product.PRODUCT_TYPE_SUPPLY,
            "last_purchase_price": 50.00,
            "sale_price": 80.00,
            "stock_quantity": 100,
            "stock_control_enabled": True,
        }
        serializer = ProductSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_product_serializer_negative_prices(self, create_profile):
        profile = create_profile()
        data = {
            "user": profile.user.id,
            "name": "Car Shampoo",
            "description": "High foam automotive shampoo",
            "unit_type": Product.UNIT_TYPE_ML,
            "product_type": Product.PRODUCT_TYPE_SUPPLY,
            "last_purchase_price": -50.00,
            "sale_price": 80.00,
            "stock_quantity": 100,
            "stock_control_enabled": True,
        }
        serializer = ProductSerializer(data=data)
        assert not serializer.is_valid()
        assert "last_purchase_price" in serializer.errors

    def test_product_serializer_negative_sale_price(self, create_profile):
        profile = create_profile()
        data = {
            "user": profile.user.id,
            "name": "Car Shampoo",
            "description": "High foam automotive shampoo",
            "unit_type": Product.UNIT_TYPE_ML,
            "product_type": Product.PRODUCT_TYPE_SUPPLY,
            "last_purchase_price": 50.00,
            "sale_price": -80.00,
            "stock_quantity": 100,
            "stock_control_enabled": True,
        }
        serializer = ProductSerializer(data=data)
        assert not serializer.is_valid()
        assert "sale_price" in serializer.errors

    def test_product_serializer_invalid_unit_type(self, create_profile):
        profile = create_profile()
        data = {
            "user": profile.user.id,
            "name": "Car Shampoo",
            "description": "High foam automotive shampoo",
            "unit_type": "invalid",
            "product_type": Product.PRODUCT_TYPE_SUPPLY,
            "last_purchase_price": 50.00,
            "sale_price": 80.00,
            "stock_quantity": 100,
            "stock_control_enabled": True,
        }
        serializer = ProductSerializer(data=data)
        assert not serializer.is_valid()
        assert "unit_type" in serializer.errors

    def test_product_serializer_invalid_product_type(self, create_profile):
        profile = create_profile()
        data = {
            "user": profile.user.id,
            "name": "Car Shampoo",
            "description": "High foam automotive shampoo",
            "unit_type": Product.UNIT_TYPE_ML,
            "product_type": "invalid",
            "last_purchase_price": 50.00,
            "sale_price": 80.00,
            "stock_quantity": 100,
            "stock_control_enabled": True,
        }
        serializer = ProductSerializer(data=data)
        assert not serializer.is_valid()
        assert "product_type" in serializer.errors

    def test_product_serializer_negative_stock_quantity(self, create_profile):
        profile = create_profile()
        data = {
            "user": profile.user.id,
            "name": "Car Shampoo",
            "description": "High foam automotive shampoo",
            "unit_type": Product.UNIT_TYPE_ML,
            "product_type": Product.PRODUCT_TYPE_SUPPLY,
            "last_purchase_price": 50.00,
            "sale_price": 80.00,
            "stock_quantity": -5,
            "stock_control_enabled": True,
        }
        serializer = ProductSerializer(data=data)
        assert not serializer.is_valid()
        assert "stock_quantity" in serializer.errors
