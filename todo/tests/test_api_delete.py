import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestApiDelete:
    def test_delete_task_response_204(self,api_client,common_user,common_task):
            task = common_task
            api_client.force_authenticate(user=common_user)
            url = reverse(
                "todo:api-v1:tasks-detail",
                kwargs={"pk": task.pk},)
            response = api_client.delete(url)
            assert response.status_code == 204

    def test_delete_task_unauthenticated(self,api_client,common_task):
            task = common_task
            url = reverse("todo:api-v1:tasks-detail",kwargs={"pk": task.pk})
            response = api_client.delete(url)
            assert response.status_code == 401

    def test_delete_task_response_404(self,api_client,common_user,common_task):
        api_client.force_authenticate(user=common_user)
        deleted_pk = common_task
        common_task.delete()
        url = reverse("todo:api-v1:tasks-detail", kwargs={"pk": deleted_pk})
        response = api_client.delete(url)
        assert response.status_code == 404
    
    