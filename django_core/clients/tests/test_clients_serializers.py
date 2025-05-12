import pytest
from clients.serializers import ClientSerializer
from clients.models import Client


@pytest.mark.django_db
class TestClientSerializer:

    def test_valid_data_creates_client(self, create_profile):
        profile = create_profile()
        data = {
            "full_name": "Maria Silva",
            "phone": "9876543210",
            "email": "maria.silva@example.com",
        }

        serializer = ClientSerializer(data=data)

        serializer.context["request"] = type("obj", (object,), {"user": profile.user})()

        assert serializer.is_valid(), serializer.errors

    def test_missing_full_name_should_fail(self):
        data = {
            "phone": "9876543210",
            "email": "maria.silva@example.com",
        }
        serializer = ClientSerializer(data=data)
        assert not serializer.is_valid()
        assert "full_name" in serializer.errors

    @pytest.mark.parametrize(
        "phone, email, is_valid",
        [
            ("1111111111", "unique@example.com", True),
            ("1111111111", "", True),
            ("", "unique@example.com", True),
            ("", "", True),
            (None, "unique@example.com", True),
            ("1111111111", None, True),
            (None, None, True),
        ],
    )
    def test_optional_fields_can_be_blank_or_null(
        self, phone, email, is_valid, create_profile
    ):
        profile = create_profile()
        data = {
            "full_name": "Valid Client",
            "phone": phone,
            "email": email,
        }
        serializer = ClientSerializer(data=data)
        serializer.context["request"] = type("obj", (object,), {"user": profile.user})()

        assert serializer.is_valid() == is_valid, serializer.errors

    def test_duplicate_email_for_same_user_should_fail(self, create_profile):
        profile = create_profile()

        Client.objects.create(
            user=profile,
            full_name="Client 1",
            email="teste@example.com",
            phone="1111111111",
        )

        data = {
            "full_name": "Client 2",
            "phone": "2222222222",
            "email": "teste@example.com",
        }
        serializer = ClientSerializer(data=data)
        serializer.context["request"] = type("obj", (object,), {"user": profile.user})()

        assert not serializer.is_valid()
        assert "message" in serializer.errors
        assert (
            "This email address is already registered for one of your clients."
            in serializer.errors["message"]
        )

    def test_duplicate_email_for_different_users_should_pass(self, create_profile):
        profile1 = create_profile(full_name="user1", username="user_1")
        profile2 = create_profile(full_name="user2", username="user_2")

        Client.objects.create(
            user=profile1,
            full_name="Client A",
            phone="1111111111",
            email="user1@example.com",
        )

        data = {
            "full_name": "Client B",
            "phone": "2222222222",
            "email": "user1@example.com",
        }
        serializer = ClientSerializer(data=data)
        serializer.context["request"] = type(
            "obj", (object,), {"user": profile2.user}
        )()

        assert serializer.is_valid(), serializer.errors
