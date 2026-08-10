import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestApiGetDetail:

    def test_get_task_detail_response_200(self,api_client,common_user,common_task):
        task = common_task
        api_client.force_authenticate(user=common_user)
        url = reverse(
            "todo:api-v1:tasks-detail",
            kwargs={"pk": task.pk},)
        response = api_client.get(url)
        assert response.status_code == 200


    def test_get_task_detail_unauthenticated(self,api_client,common_task):
        task = common_task
        url = reverse("todo:api-v1:tasks-detail",kwargs={"pk": task.pk})
        response = api_client.get(url)
        assert response.status_code == 401


    def test_get_nonexistent_task(self,api_client,common_user):
        api_client.force_authenticate(user=common_user)
        url = reverse("todo:api-v1:tasks-detail",kwargs={"pk": 99999},)
        response = api_client.get(url)
        assert response.status_code == 404