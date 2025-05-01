import pytest
from decimal import Decimal
from rest_framework import status
from services.models import Service, ServiceProduct

CREATE_URL = "/api/services/"
LIST_URL = "/api/services/"
RETRIEVE_URL = "/api/services/{}/"
UPDATE_URL = "/api/services/{}/"
DELETE_URL = "/api/services/{}/"


@pytest.mark.django_db
class TestServiceView:

    def test_create_service(self, api_client, create_profile, create_product):
        """Tests the creation of a service with valid data."""
        profile = create_profile()
        api_client.force_authenticate(user=profile.user)

        product1 = create_product(
            profile=profile, name="Foam Cleaner", last_purchase_price="25.00"
        )
        product2 = create_product(
            profile=profile, name="Glass Cleaner", last_purchase_price="10.00"
        )

        data = {
            "user": profile.user.id,
            "name": "Full Car Cleaning",
            "description": "Complete interior and exterior cleaning",
            "pricing_type": Service.PRICING_TYPE_FIXED,
            "base_price": "250.00",
            "estimated_time": 120,
            "products": [
                {"product": str(product1.id), "quantity": "2.0"},
                {"product": str(product2.id), "quantity": "1.5"},
            ],
        }

        response = api_client.post(CREATE_URL, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Service.objects.count() == 1
        assert ServiceProduct.objects.count() == 2

        service = Service.objects.first()
        service_product1 = service.serviceproduct_set.get(product=product1)
        service_product2 = service.serviceproduct_set.get(product=product2)

        assert service.name == "Full Car Cleaning"
        assert service.serviceproduct_set.count() == 2

        assert service_product1.product == product1
        assert service_product1.quantity == 2.0

        assert service_product2.product == product2
        assert service_product2.quantity == 1.5

    def test_list_services(self, api_client, create_profile, create_service):
        """Tests the listing of services."""
        profile = create_profile()
        api_client.force_authenticate(user=profile.user)

        create_service(profile=profile)

        response = api_client.get(LIST_URL)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_retrieve_service(self, api_client, create_profile, create_service):
        """Tests the retrieval of a specific service."""
        profile = create_profile()
        api_client.force_authenticate(user=profile.user)

        service = create_service(profile=profile)

        response = api_client.get(RETRIEVE_URL.format(service.id))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == service.name
        assert response.data["description"] == service.description
        assert response.data["pricing_type"] == service.pricing_type
        assert Decimal(response.data["base_price"]) == service.base_price
        assert response.data["estimated_time"] == service.estimated_time

    def test_update_service(
        self,
        api_client,
        create_profile,
        create_service,
        create_product,
        add_product_to_service,
    ):
        """Tests the update of a service."""
        profile = create_profile()
        api_client.force_authenticate(user=profile.user)

        service = create_service(profile=profile)
        product = create_product(
            profile=profile, name="Foam Cleaner", last_purchase_price="25.00"
        )
        add_product_to_service(service=service, product=product, quantity=45)
        updated_data = {
            "name": "Updated Full Car Cleaning",
            "description": service.description,
            "pricing_type": service.pricing_type,
            "base_price": service.base_price,
            "estimated_time": service.estimated_time,
            "products": [
                {"product": str(sp.product_id), "quantity": str(sp.quantity)}
                for sp in service.serviceproduct_set.all()
            ],
        }

        response = api_client.patch(UPDATE_URL.format(service.id), updated_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Full Car Cleaning"
        assert response.data["user"] == profile.user.id

    def test_update_service_with_new_products(
        self,
        api_client,
        create_profile,
        create_service,
        create_product,
        add_product_to_service,
    ):
        """Tests updating a service with new associated products, replacing the previous ones."""
        profile = create_profile()
        api_client.force_authenticate(user=profile.user)

        service = create_service(profile=profile)
        old_product = create_product(
            profile=profile, name="Old Cleaner", last_purchase_price="10.00"
        )
        add_product_to_service(service=service, product=old_product, quantity=10)

        new_product1 = create_product(
            profile=profile, name="New Shampoo", last_purchase_price="20.00"
        )
        new_product2 = create_product(
            profile=profile, name="Glass Cleaner", last_purchase_price="15.00"
        )

        updated_data = {
            "name": service.name,
            "description": service.description,
            "pricing_type": service.pricing_type,
            "base_price": str(service.base_price),
            "estimated_time": service.estimated_time,
            "products": [
                {"product": str(new_product1.id), "quantity": "2.5"},
                {"product": str(new_product2.id), "quantity": "1.0"},
            ],
        }

        response = api_client.patch(
            UPDATE_URL.format(service.id), updated_data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK

        product_ids = set({product["product"] for product in response.data["products"]})
        assert product_ids == {str(new_product1.id), str(new_product2.id)}

    def test_delete_service(
        self,
        api_client,
        create_profile,
        create_service,
        create_product,
        add_product_to_service,
    ):
        """Tests the deletion of a service."""
        profile = create_profile()
        api_client.force_authenticate(user=profile.user)

        service = create_service(profile=profile)
        produduct = create_product(profile=profile)
        add_product_to_service(service=service, product=produduct, quantity=10)

        response = api_client.delete(DELETE_URL.format(service.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = api_client.get(RETRIEVE_URL.format(service.id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_service_with_invalid_data(
        self, api_client, create_profile, create_product
    ):
        """Tests the creation of a service with invalid data."""
        profile = create_profile()
        api_client.force_authenticate(user=profile.user)

        product = create_product(profile=profile)
        data = {
            "name": "",
            "pricing_type": Service.PRICING_TYPE_FIXED,
            "base_price": "250.00",
            "estimated_time": 120,
            "products": [
                {"product": str(product.id), "quantity": "2.0"},
            ],
        }

        response = api_client.post(CREATE_URL, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data
        assert "description" in response.data

    def test_update_service_missing_required_fields(
        self,
        api_client,
        create_profile,
        create_service,
        create_product,
        add_product_to_service,
    ):
        """Tests updating a service with missing required fields."""
        profile = create_profile()
        api_client.force_authenticate(user=profile.user)

        service = create_service(profile=profile)
        product = create_product(profile=profile)
        add_product_to_service(service=service, product=product, quantity=10)

        data = {"name": ""}

        response = api_client.patch(UPDATE_URL.format(service.id), data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_unauthenticated_access(self, api_client, create_service):
        """Tests that unauthenticated users cannot access the routes."""
        service = create_service()

        response = api_client.post(CREATE_URL, {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = api_client.get(RETRIEVE_URL.format(service.id))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_access_other_user_service(
        self, api_client, create_user, create_profile, create_service, create_product
    ):
        """Tests that a user cannot access or edit another user's services."""
        user1 = create_user(username="user1", password="password123")
        profile1 = create_profile(user=user1)
        user2 = create_user(username="user2", password="password123")
        profile2 = create_profile(user2)

        service = create_service(profile=profile1)
        api_client.force_authenticate(user=profile2.user)

        response = api_client.get(RETRIEVE_URL.format(service.id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

        data = {"name": "Should Not Work"}
        response = api_client.patch(UPDATE_URL.format(service.id), data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
