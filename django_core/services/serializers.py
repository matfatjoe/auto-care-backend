from rest_framework import serializers
from services.models import Service, ServiceProduct
from products.models import Product


class ServiceProductUsageSerializer(serializers.Serializer):
    product = serializers.UUIDField()
    quantity = serializers.DecimalField(
        max_digits=10, decimal_places=2, allow_null=True
    )

    def validate_quantity(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return float(value)


class ServiceSerializer(serializers.ModelSerializer):
    products = ServiceProductUsageSerializer(many=True, required=False)

    class Meta:
        model = Service
        fields = [
            "id",
            "user",
            "name",
            "description",
            "pricing_type",
            "base_price",
            "estimated_time",
            "products",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def validate_base_price(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Base price must be greater than 0.")
        return value

    def create(self, validated_data):
        products_data = validated_data.pop("products", [])
        user = validated_data["user"]

        product_ids = [p["product"] for p in products_data]
        existing_products = Product.objects.filter(id__in=product_ids).values_list(
            "id", flat=True
        )

        missing_products = set(product_ids) - set(existing_products)
        if missing_products:
            raise serializers.ValidationError(
                {"message": "One or more products do not exist."}
            )

        service = Service.objects.create(**validated_data)

        for product_data in products_data:
            ServiceProduct.objects.create(
                service=service,
                product_id=product_data["product"],
                quantity=product_data["quantity"],
                user=user,
            )
        return service
