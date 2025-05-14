import pytest
from rest_framework import status

CREATE_URL = "/api/clients/"
LIST_URL = "/api/clients/"
RETRIEVE_URL = "/api/clients/{}/"
UPDATE_URL = "/api/clients/{}/"
DELETE_URL = "/api/clients/{}/"


@pytest.mark.django_db
class TestClientView:
    def test_create_client(self, api_client, create_profile):
        """Tests the creation of a client with valid data."""
        profile = create_profile()
        api_client.force_authenticate(user=profile.user)

        data = {
            "user": profile.user.id,
            "full_name": "John Doe",
            "phone": "1111111111",
            "email": "johndoe@example.com",
        }

        response = api_client.post(CREATE_URL, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert response.data["full_name"] == "John Doe"
        assert response.data["user"] == profile.user.id
        assert response.data["phone"] == "1111111111"
        assert response.data["email"] == "johndoe@example.com"

    def test_list_clients(self, api_client, create_profile, create_client):
        """Tests the listing of clients."""
        profile = create_profile()
        create_client(profile=profile)

        api_client.force_authenticate(user=profile.user)
        response = api_client.get(LIST_URL)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_retrieve_client(self, api_client, create_profile, create_client):
        """Tests the retrieval of a specific client."""
        profile = create_profile()

        client = create_client(profile=profile)
        api_client.force_authenticate(user=profile.user)

        response = api_client.get(RETRIEVE_URL.format(client.id))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(client.id)
        assert response.data["full_name"] == client.full_name
        assert response.data["phone"] == client.phone
        assert response.data["email"] == client.email
        assert response.data["user"] == profile.user.id

    def test_update_client(self, api_client, create_profile, create_client):
        """Tests the update of a client."""
        profile = create_profile()

        client = create_client(profile=profile)
        api_client.force_authenticate(user=profile.user)

        updated_data = {
            "full_name": "Updated John Doe",
            "phone": "22222222222",
            "email": "johndoe@dev.com",
        }

        response = api_client.patch(UPDATE_URL.format(client.id), updated_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["full_name"] == "Updated John Doe"
        assert response.data["user"] == profile.user.id
        assert response.data["phone"] == "22222222222"
        assert response.data["email"] == "johndoe@dev.com"

    def test_delete_client(self, api_client, create_profile, create_client):
        """Tests the deletion of a client."""
        profile = create_profile()

        client = create_client(profile=profile)
        api_client.force_authenticate(user=profile.user)

        response = api_client.delete(UPDATE_URL.format(client.id))

        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = api_client.get(RETRIEVE_URL.format(client.id))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_client_invalid_data(self, api_client, create_profile):
        """Tests the failure to create a client with invalid data."""
        profile = create_profile()
        api_client.force_authenticate(user=profile.user)

        data = {
            "user": profile.user.id,
            "full_name": "",
            "phone": "aaaa",
            "email": "1111",
        }

        response = api_client.post(CREATE_URL, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "full_name" in response.data
        assert "email" in response.data

    def test_update_client_missing_required_fields(
        self, api_client, create_profile, create_client
    ):
        """Tests the failure to update with incomplete data."""
        profile = create_profile()
        client = create_client(profile=profile)
        api_client.force_authenticate(user=profile.user)

        data = {"full_name": ""}

        response = api_client.patch(UPDATE_URL.format(client.id), data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "full_name" in response.data

    def test_unauthenticated_access(self, api_client, create_client):
        """Tests that unauthenticated users cannot access the routes."""
        client = create_client()

        response = api_client.get(RETRIEVE_URL.format(client.id))
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = api_client.post(CREATE_URL, {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_access_other_user_client(
        self, api_client, create_user, create_profile, create_client
    ):
        """Tests that a user cannot access or edit another user's clients."""
        user1 = create_user(username="user1", password="password123")
        profile1 = create_profile(user=user1)
        user2 = create_user(username="user2", password="password123")
        profile2 = create_profile(user2)
        client = create_client(profile=profile1)
        api_client.force_authenticate(user=profile2.user)

        response = api_client.get(RETRIEVE_URL.format(client.id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

        data = {"full_name": "Should Not Work"}
        response = api_client.patch(UPDATE_URL.format(client.id), data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
