import pytest
from rest_framework import status
from products.models import Product


CREATE_URL = "/api/products/"
LIST_URL = "/api/products/"
RETRIEVE_URL = "/api/products/{}/"
UPDATE_URL = "/api/products/{}/"
DELETE_URL = "/api/products/{}/"


@pytest.mark.django_db
class TestProductView:
    def test_create_product(self, api_client, create_profile):
        """Tests the creation of a product with valid data."""
        profile = create_profile()

        api_client.force_authenticate(user=profile.user)

        data = {
            "user": profile.user.id,
            "name": "Car Shampoo",
            "description": "High foam automotive shampoo",
            "unit_type": Product.UNIT_TYPE_ML,
            "product_type": Product.PRODUCT_TYPE_SUPPLY,
            "last_purchase_price": 50.00,
            "sale_price": 80.00,
            "stock_quantity": 100,
            "stock_control_enabled": True,
        }

        response = api_client.post(CREATE_URL, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert response.data["name"] == "Car Shampoo"
        assert response.data["user"] == profile.user.id

    def test_list_products(self, api_client, create_profile, product_supply):
        """Tests the listing of products."""
        profile = create_profile()

        product_supply(profile=profile)
        api_client.force_authenticate(user=profile.user)

        response = api_client.get(LIST_URL)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_retrieve_product(self, api_client, create_profile, product_supply):
        """Tests the retrieval of a specific product."""
        profile = create_profile()

        product = product_supply(profile=profile)
        api_client.force_authenticate(user=profile.user)

        response = api_client.get(RETRIEVE_URL.format(product.id))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == product.name
        assert response.data["description"] == product.description
        assert response.data["unit_type"] == product.unit_type

    def test_update_product(self, api_client, create_profile, product_supply):
        """Tests the update of a product."""
        profile = create_profile()

        product = product_supply(profile=profile)
        api_client.force_authenticate(user=profile.user)

        updated_data = {
            "name": "Updated Car Shampoo",
            "description": product.description,
            "unit_type": product.unit_type,
            "product_type": product.product_type,
            "last_purchase_price": product.last_purchase_price,
            "sale_price": product.sale_price,
            "stock_quantity": product.stock_quantity,
            "stock_control_enabled": product.stock_control_enabled,
        }

        response = api_client.patch(UPDATE_URL.format(product.id), updated_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Car Shampoo"
        assert response.data["user"] == profile.user.id

    def test_delete_product(self, api_client, create_profile, product_supply):
        """Tests the deletion of a product."""
        profile = create_profile()

        product = product_supply(profile=profile)
        api_client.force_authenticate(user=profile.user)

        response = api_client.delete(UPDATE_URL.format(product.id))

        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = api_client.get(RETRIEVE_URL.format(product.id))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_product_invalid_data(self, api_client, create_profile):
        """Tests the failure to create a product with invalid data."""
        profile = create_profile()
        api_client.force_authenticate(user=profile.user)

        data = {
            "name": "",
            "unit_type": Product.UNIT_TYPE_ML,
            "product_type": Product.PRODUCT_TYPE_SUPPLY,
            "last_purchase_price": -10.00,
            "sale_price": -5.00,
            "stock_quantity": -1,
            "stock_control_enabled": True,
        }

        response = api_client.post(CREATE_URL, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data
        assert "description" in response.data
        assert "last_purchase_price" in response.data
        assert "sale_price" in response.data
        assert "stock_quantity" in response.data
    def test_update_product_missing_required_fields(self, api_client, create_profile, product_supply):
        """Tests the failure to update with incomplete data."""
        profile = create_profile()
        product = product_supply(profile=profile)
        api_client.force_authenticate(user=profile.user)

        data = {
            "name": ""
        }

        response = api_client.patch(UPDATE_URL.format(product.id), data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_unauthenticated_access(self, api_client, product_supply):
        """Tests that unauthenticated users cannot access the routes."""
        product = product_supply()

        response = api_client.get(RETRIEVE_URL.format(product.id))
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = api_client.post(CREATE_URL, {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_access_other_user_product(self, api_client, create_user, create_profile, product_supply):
        """Tests that a user cannot access or edit another user's products."""
        user1 = create_user(username="user1", password="password123")
        profile1 = create_profile(user=user1)
        
        user2 = create_user(username="user2", password="password123")
        profile2 = create_profile(user2)
        product = product_supply(profile=profile1)
        api_client.force_authenticate(user=profile2.user)

        response = api_client.get(RETRIEVE_URL.format(product.id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

        data = {"name": "Should Not Work"}
        response = api_client.patch(UPDATE_URL.format(product.id), data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
