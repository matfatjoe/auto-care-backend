from django.contrib.auth import authenticate
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

        Profile.objects.create(user=user, full_name="", phone="")

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Usuário ou senha inválidos.")
        data["user"] = user
        return data


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
