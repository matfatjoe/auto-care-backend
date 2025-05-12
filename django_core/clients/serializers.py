from rest_framework import serializers
from clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Client
        fields = [
            "id",
            "user",
            "full_name",
            "phone",
            "email",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def validate_last_purchase_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Last purchase price cannot be negative.")
        return value

    def validate(self, data):
        user = self.context["request"].user.profile
        email = data.get("email")

        instance = self.instance
        if email and email.strip():
            qs = Client.objects.filter(user=user, email=email)
            if instance:
                qs = qs.exclude(id=instance.id)
            if qs.exists():
                raise serializers.ValidationError(
                    {
                        "message": "This email address is already registered for one of your clients."
                    }
                )
        return data
