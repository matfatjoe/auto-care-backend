from django.contrib.auth.models import User
from rest_framework import serializers
from authentication.models import Profile


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Criação automática do Profile
        Profile.objects.create(user=user, full_name="", phone="")

        return user
