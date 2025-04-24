from rest_framework import status
from django.contrib.auth.models import User
import pytest

LOGIN_URL = "/api/auth/login"
LOGOUT_URL = "/api/auth/logout"
REGISTER_URL = "/api/auth/register"


class RegistrationPayload:
    """Groups the payload data for user registration."""

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def as_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }


@pytest.mark.django_db
class TestLoginView:

    def test_can_login_with_valid_credentials(self, api_client, create_user):
        """Tests successful login with valid credentials."""
        user = create_user()
        response = api_client.post(
            LOGIN_URL, {"username": user.username, "password": "secret123"})
        assert response.status_code == status.HTTP_200_OK
        assert "username" in response.data
        assert response.data["username"] == user.username

    def test_cannot_login_with_invalid_credentials(self, api_client):
        """Tests login with invalid credentials."""
        response = api_client.post(
            LOGIN_URL, {"username": "invalid", "password": "wrong"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data

    def test_cannot_login_with_missing_fields(self, api_client):
        """Tests login with missing fields."""
        response = api_client.post(LOGIN_URL, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data
        assert "password" in response.data

    def test_cannot_login_with_invalid_field_type(self, api_client):
        """Tests login with invalid field types."""
        response = api_client.post(
            LOGIN_URL, {"username": ["not", "a", "string"], "password": "pass"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_login_with_inactive_user(self, api_client, create_user):
        """Tests login with an inactive user."""
        user = create_user(is_active=False)
        response = api_client.post(
            LOGIN_URL, {"username": user.username, "password": "secret123"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogoutView:

    @pytest.fixture(autouse=True)
    def setup_logout_test(self, api_client, create_user):
        """Sets up a logged-in user for logout tests."""
        self.user = create_user(username='testuser', password='testpass123')
        self.api_client = api_client
        self.api_client.login(username='testuser', password='testpass123')

    def test_can_logout_authenticated_user(self):
        """Tests the logout of an authenticated user."""
        response = self.api_client.post(LOGOUT_URL)
        assert response.status_code == status.HTTP_200_OK
        # Keeping original Portuguese message as per previous code
        assert response.data['detail'] == 'Logout realizado com sucesso.'

    def test_cannot_logout_unauthenticated_user(self, api_client):
        """Tests the logout of an unauthenticated user."""
        api_client.logout()
        response = api_client.post(LOGOUT_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert 'detail' in response.data
        # Keeping original Portuguese message as per previous code
        assert response.data['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
class TestUserRegistrationView:

    def test_can_register_valid_user(self, api_client):
        """Tests the successful registration of a new user."""
        payload = RegistrationPayload(
            "newuser", "newuser@example.com", "newpassword123")
        response = api_client.post(REGISTER_URL, data=payload.as_dict())

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username=payload.username).exists()
        assert "id" in response.data
        assert response.data["username"] == payload.username
        assert response.data["email"] == payload.email

    def test_cannot_register_with_missing_fields(self, api_client):
        """Tests registration with missing fields."""
        response = api_client.post(REGISTER_URL, data={})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data
        assert "password" in response.data

    def test_cannot_register_with_duplicate_username(self, api_client, create_user):
        """Tests registration with a duplicate username."""
        create_user(username="duplicated")
        payload = RegistrationPayload(
            "duplicated", "duplicate@example.com", "anotherpass")
        response = api_client.post(REGISTER_URL, data=payload.as_dict())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data


@pytest.mark.django_db
class TestUserAuthFlow:

    def test_can_register_and_login_user(self, api_client):
        """Tests full flow: register a user and then login successfully."""

        payload = RegistrationPayload(
            "newuser", "newuser@example.com", "newpassword123")

        register_response = api_client.post(
            REGISTER_URL, data=payload.as_dict())
        assert register_response.status_code == status.HTTP_201_CREATED
        assert register_response.data["username"] == payload.username

        login_payload = {
            "username": payload.username,
            "password": payload.password
        }

        login_response = api_client.post(LOGIN_URL, data=login_payload)
        assert login_response.status_code == status.HTTP_200_OK
        assert login_response.data["username"] == payload.username
