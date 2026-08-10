import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestApiGet:
    def test_get_task_response_200(self, api_client,common_user):
        url = reverse("todo:api-v1:tasks-list")
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_get_task_response_401(self, api_client,common_user):
        url = reverse("todo:api-v1:tasks-list")
        response = api_client.get(url)
        assert response.status_code == 401


    

