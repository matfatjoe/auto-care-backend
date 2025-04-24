import pytest
from django.contrib.auth.models import User
from authentication.models import Profile
from django.utils.timezone import now
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestProfileModel:

    def test_profile_creation(self):
        user = User.objects.create_user(username="johndoe", password="123456")
        profile = Profile.objects.create(
            user=user,
            full_name="John Doe",
            phone="+55 11 99999-0000",
        )

        assert profile.user == user
        assert profile.full_name == "John Doe"
        assert profile.phone == "+55 11 99999-0000"
        assert profile.created_at is not None
        assert profile.updated_at is not None

    def test_profile_str_method(self):
        user = User.objects.create_user(username="janedoe", password="abcdef")
        profile = Profile.objects.create(
            user=user,
            full_name="Jane Doe",
            phone="(21) 98765-4321",
        )

        assert str(profile) == "Jane Doe"

    def test_profile_user_relationship(self):
        user = User.objects.create_user(username="mike", password="123123")
        profile = Profile.objects.create(
            user=user, full_name="Mike Tyson", phone="1234")
        assert user.profile == profile

    def test_created_at_and_updated_at_are_set(self):
        user = User.objects.create_user(
            username="createduser", password="321321")
        profile = Profile.objects.create(
            user=user, full_name="Time Test", phone="0000")

        assert profile.created_at <= now()
        assert profile.updated_at <= now()

    def test_updated_at_changes_on_save(self):
        user = User.objects.create_user(
            username="updateuser", password="update123")
        profile = Profile.objects.create(
            user=user, full_name="Before Update", phone="123")

        original_updated_at = profile.updated_at
        profile.full_name = "After Update"
        profile.save()

        profile.refresh_from_db()
        assert profile.updated_at > original_updated_at

    def test_missing_required_fields(self):
        user = User.objects.create_user(
            username="failuser", password="fail123")
        profile = Profile(user=user)

        with pytest.raises(ValidationError):
            profile.full_clean()
