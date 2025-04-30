from rest_framework import serializers
from services.models import Service


class ServiceSerializer(serializers.ModelSerializer):
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
        ]
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def validate_base_price(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Base price must be greater than 0.")
        return value
