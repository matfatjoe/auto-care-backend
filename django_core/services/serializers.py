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
            "is_deleted",
            "created_at",
            "updated_at",
            "deleted_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]
        extra_kwargs = {
            "user": {"read_only": True},
            "is_deleted": {"write_only": True},
        }
