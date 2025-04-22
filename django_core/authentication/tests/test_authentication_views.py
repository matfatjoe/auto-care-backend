from rest_framework.authtoken.models import Token
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


# @pytest.mark.django_db
# class TestLoginView:

#     @pytest.fixture
#     def client(self):
#         return APIClient()

#     @pytest.fixture
#     def user(self):
#         return User.objects.create_user(username="johndoe", email="john@example.com", password="secret123")

#     def test_successful_login(self, client, user):
#         response = client.post(
#             "/api/auth/login/", {"username": "johndoe", "password": "secret123"})
#         assert response.status_code == status.HTTP_200_OK
#         assert "username" in response.data

#     def test_invalid_credentials(self, client):
#         response = client.post(
#             "/api/auth/login/", {"username": "invalid", "password": "wrong"})
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert "non_field_errors" in response.data

#     def test_missing_fields(self, client):
#         response = client.post("/api/auth/login/", {})
#         assert response.status_code == 400
#         assert "username" in response.data
#         assert "password" in response.data

#     def test_invalid_field_type(self, client):
#         response = client.post(
#             "/api/auth/login/", {"username": ["not", "a", "string"], "password": "pass"})
#         assert response.status_code == 400

#     def test_inactive_user(self, client, user):
#         user.is_active = False
#         user.save()
#         response = client.post(
#             "/api/auth/login/", {"username": "johndoe", "password": "secret123"})
#         assert response.status_code == 400


@pytest.mark.django_db
class TestLogoutView:

    def setup_method(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')
        self.client = APIClient()

        self.client.login(username='testuser', password='testpass123')

    def test_logout_authenticated_user(self):
        response = self.client.post('/api/auth/logout/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['detail'] == 'Logout realizado com sucesso.'

    def test_logout_unauthenticated_user(self):
        self.client.logout()
        response = self.client.post('/api/auth/logout/')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert 'detail' in response.data
        assert response.data['detail'] == 'Authentication credentials were not provided.'
