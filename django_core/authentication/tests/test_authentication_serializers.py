import pytest
from django.contrib.auth.models import User
from authentication.serializers import UserRegistrationSerializer


@pytest.mark.django_db
class TestUserRegistrationSerializer:

    def test_valid_data_creates_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123"
        }
        serializer = UserRegistrationSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

        user = serializer.save()
        assert User.objects.filter(username="newuser").exists()
        assert user.profile.full_name == ""

    def test_missing_fields(self):
        serializer = UserRegistrationSerializer(data={})
        assert not serializer.is_valid()
        assert "username" in serializer.errors
        assert "email" in serializer.errors
        assert "password" in serializer.errors

    def test_short_password_is_invalid(self):
        data = {
            "username": "shortpassuser",
            "email": "short@example.com",
            "password": "123"
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_duplicate_username_fails(self):
        User.objects.create_user(username="duplicated", password="testpass")
        data = {
            "username": "duplicated",
            "email": "other@example.com",
            "password": "somepassword"
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors
