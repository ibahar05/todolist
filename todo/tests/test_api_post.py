import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestAPIPost:
    def test_create_post_with_valid_data(self,api_client,common_user):
        url = reverse("todo:api-v1:tasks-list")
        data = {
            "title": "test title",
            "is_completed": False,
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url,data)
        assert response.status_code == 201

    def test_create_post_with_invalid_data(self,api_client,common_user):
            url = reverse("todo:api-v1:tasks-list")
            data = {
                "is_completed": False,
            }
            user = common_user
            api_client.force_authenticate(user=user)
            response = api_client.post(url,data)
            assert response.status_code == 400

    def test_create_post_response_401(self,api_client):
        url = reverse("todo:api-v1:tasks-list")
        data = {
                "title": "test title",
                "is_completed": False,
             }
        response = api_client.post(url,data)
        assert response.status_code == 401

    






