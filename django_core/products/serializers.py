from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "user",
            "name",
            "description",
            "unit_type",
            "product_type",
            "last_purchase_price",
            "sale_price",
            "stock_quantity",
            "stock_control_enabled",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "user": {"read_only": True},
            "is_deleted": {"write_only": True},
        }

    def validate_last_purchase_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Last purchase price cannot be negative.")
        return value

    def validate_sale_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Sale price cannot be negative.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value

    def validate_unit_type(self, value):
        allowed_types = [choice[0] for choice in Product.UNIT_TYPE_CHOICES]
        if value not in allowed_types:
            raise serializers.ValidationError("Invalid item_type.")
        return value

    def validate_product_type(self, value):
        allowed_types = [choice[0] for choice in Product.PRODUCT_TYPE_CHOICES]
        if value not in allowed_types:
            raise serializers.ValidationError("Invalid product type.")
        return value
