import pytest
from django.core.exceptions import ValidationError
from clients.models import Client


@pytest.mark.django_db
class TestClientModel:

    def test_create_client_successfully(self, create_profile):
        profile = create_profile()
        client = Client.objects.create(
            user=profile,
            full_name="New Client",
            phone="4199999999",
            email="test@teste.com",
        )

        assert client.id is not None
        assert client.user == profile
        assert client.full_name == "New Client"
        assert client.phone == "4199999999"
        assert client.email == "test@teste.com"
        assert client.is_deleted is False
        assert client.created_at is not None
        assert client.updated_at is not None

    def test_cannot_create_client_without_full_name(self, create_profile):
        profile = create_profile()
        with pytest.raises(ValidationError):
            Client.objects.create(
                user=profile, full_name="", phone="4199999999", email="test@teste"
            ).full_clean()

    def test_cannot_create_client_without_phone(self, create_profile):
        profile = create_profile()
        with pytest.raises(ValidationError):
            Client.objects.create(
                user=profile, full_name="New Client", phone="", email="test@teste"
            ).full_clean()

    def test_cannot_create_client_without_email(self, create_profile):
        profile = create_profile()
        with pytest.raises(ValidationError):
            Client.objects.create(
                user=profile, full_name="New Client", phone="4199999999", email=""
            ).full_clean()

    def test_cannot_create_client_with_invalid_email(self, create_profile):
        profile = create_profile()
        with pytest.raises(ValidationError):
            Client.objects.create(
                user=profile,
                full_name="New Client",
                phone="4199999999",
                email="invalid_email",
            ).full_clean()

    def test_cannot_create_client_with_invalid_phone(self, create_profile):
        profile = create_profile()
        with pytest.raises(ValidationError):
            Client.objects.create(
                user=profile,
                full_name="New Client",
                phone="invalid_phone",
                email="test@teste",
            ).full_clean()
