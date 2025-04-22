import pytest
from django.contrib.auth.models import User
from authentication.serializers import UserRegistrationSerializer, UserLoginSerializer


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


@pytest.mark.django_db
class TestUserLoginSerializer:

    def setup_method(self):
        self.user = User.objects.create_user(
            username="johndoe",
            email="john@example.com",
            password="securepass123"
        )

    def test_valid_login_returns_user(self):
        data = {"username": "johndoe", "password": "securepass123"}
        serializer = UserLoginSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["user"] == self.user

    def test_login_fails_with_invalid_username(self):
        data = {"username": "wronguser", "password": "securepass123"}
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    def test_login_fails_with_wrong_password(self):
        data = {"username": "johndoe", "password": "wrongpass"}
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    def test_login_fails_with_missing_fields(self):
        serializer = UserLoginSerializer(data={})
        assert not serializer.is_valid()
        assert "username" in serializer.errors
        assert "password" in serializer.errors

    def test_login_with_inactive_user(self):
        user = User.objects.create_user(
            username='inactive', password='testpass123')
        user.is_active = False
        user.save()

        data = {'username': 'inactive', 'password': 'testpass123'}
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors
