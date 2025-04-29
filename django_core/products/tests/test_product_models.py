import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from products.models import Product
from authentication.models import Profile


@pytest.mark.django_db
class TestProductModel:

    def setup_method(self):
        self.user = User.objects.create_user(username="john_doe", password="password123")
        self.profile = Profile.objects.create(
            user=self.user,
            full_name="John Doe",
            phone="1234567890"
        )

    def test_create_product_successfully(self):
        product = Product.objects.create(
            user=self.profile,
            name="Car Shampoo",
            description="High foam automotive shampoo",
            unit_type=Product.UNIT_TYPE_ML,
            product_type=Product.PRODUCT_TYPE_SUPPLY,
            last_purchase_price=50.00,
            sale_price=80.00,
            stock_quantity=100,
            stock_control_enabled=True,
        )

        assert product.name == "Car Shampoo"
        assert product.user == self.profile
        assert product.unit_type == Product.UNIT_TYPE_ML
        assert product.product_type == Product.PRODUCT_TYPE_SUPPLY
        assert product.last_purchase_price == 50.00
        assert product.sale_price == 80.00
        assert product.stock_quantity == 100
        assert product.stock_control_enabled is True

    def test_cannot_create_product_without_name(self):
        with pytest.raises(ValidationError):
            Product.objects.create(
                user=self.profile,
                name=None,
                description="High foam automotive shampoo",
                unit_type=Product.UNIT_TYPE_ML,
                product_type=Product.PRODUCT_TYPE_SUPPLY,
                last_purchase_price=50.00,
                sale_price=80.00,
                stock_quantity=100,
                stock_control_enabled=True,
            )

    def test_cannot_create_product_without_last_purchase_price(self):
        with pytest.raises(ValidationError):
            Product.objects.create(
                user=self.profile,
                name="Car Shampoo",
                description="High foam automotive shampoo",
                unit_type=Product.UNIT_TYPE_ML,
                product_type=Product.PRODUCT_TYPE_SUPPLY,
                last_purchase_price=None,
                sale_price=80.00,
                stock_quantity=100,
                stock_control_enabled=True,
            )

    def test_cannot_create_product_without_sale_price(self):
        with pytest.raises(ValidationError):
            product = Product.objects.create(
                user=self.profile,
                name="Car Shampoo",
                description="High foam automotive shampoo",
                unit_type=Product.UNIT_TYPE_ML,
                product_type=Product.PRODUCT_TYPE_SUPPLY,
                last_purchase_price=50.00,
                sale_price=None,
                stock_quantity=100,
                stock_control_enabled=True,
            )
            product.full_clean()

    def test_cannot_create_product_with_negative_stock_quantity(self):
        with pytest.raises(ValidationError):
            Product(
                user=self.profile,
                name="Car Shampoo",
                description="High foam automotive shampoo",
                unit_type=Product.UNIT_TYPE_ML,
                product_type=Product.PRODUCT_TYPE_SUPPLY,
                last_purchase_price=50.00,
                sale_price=80.00,
                stock_quantity=-5,
                stock_control_enabled=True,
            ).full_clean()

    def test_cannot_create_product_with_negative_prices(self):
        with pytest.raises(ValidationError):
            Product(
                user=self.profile,
                name="Car Shampoo",
                description="High foam automotive shampoo",
                unit_type=Product.UNIT_TYPE_ML,
                product_type=Product.PRODUCT_TYPE_SUPPLY,
                last_purchase_price=-10.00,
                sale_price=80.00,
                stock_quantity=10,
                stock_control_enabled=True,
            ).full_clean()

    def test_cannot_create_product_without_user(self):
        with pytest.raises(ValidationError):
            product = Product(
                user=None,
                name="Car Shampoo",
                description="High foam automotive shampoo",
                unit_type=Product.UNIT_TYPE_ML,
                product_type=Product.PRODUCT_TYPE_SUPPLY,
                last_purchase_price=50.00,
                sale_price=80.00,
                stock_quantity=100,
                stock_control_enabled=True,
            )
            product.full_clean()

    def test_default_stock_control_enabled_is_true(self):
        product = Product.objects.create(
            user=self.profile,
            name="Car Shampoo",
            description="High foam automotive shampoo",
            unit_type=Product.UNIT_TYPE_ML,
            product_type=Product.PRODUCT_TYPE_SUPPLY,
            last_purchase_price=50.00,
            sale_price=80.00,
            stock_quantity=100,
        )
        assert product.stock_control_enabled is True

    def test_product_type_should_be_valid_enum(self):
        with pytest.raises(ValidationError):
            Product(
                user=self.profile,
                name="Car Shampoo",
                description="High foam automotive shampoo",
                unit_type=Product.UNIT_TYPE_ML,
                product_type="invalid_type",
                last_purchase_price=50.00,
                sale_price=80.00,
                stock_quantity=100,
                stock_control_enabled=True,
            ).full_clean()

    def test_unit_type_should_be_valid_enum(self):
        with pytest.raises(ValidationError):
            Product(
                user=self.profile,
                name="Car Shampoo",
                description="High foam automotive shampoo",
                unit_type="invalid_unit",
                product_type=Product.PRODUCT_TYPE_SUPPLY,
                last_purchase_price=50.00,
                sale_price=80.00,
                stock_quantity=100,
                stock_control_enabled=True,
            ).full_clean()
