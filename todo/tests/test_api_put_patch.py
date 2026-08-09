import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestApiPutPatch:

    def test_put_task_response_200(self,api_client,common_user,common_task):
        task = common_task
        api_client.force_authenticate(user=common_user)
        url = reverse("todo:api-v1:tasks-detail",kwargs={"pk": task.pk},)
        data = {
                    "title": "test title2",
                    "is_completed": False,
                }
        response = api_client.put(url,data)
        assert response.status_code == 200

    def test_put_task_response_404(self,api_client,common_user):
            api_client.force_authenticate(user=common_user)
            url = reverse("todo:api-v1:tasks-detail",kwargs={"pk":259558123959416641541545455},)
            data = {
                        "title": "test title2",
                        "is_completed": False,
                    }
            response = api_client.put(url,data)
            assert response.status_code == 404

    def test_put_task_response_401(self,api_client,common_task):
            task = common_task
            url = reverse("todo:api-v1:tasks-detail",kwargs={"pk": task.pk},)
            data = {
                    "title": "test title2",
                    "is_completed": False,
                    }
            response = api_client.put(url,data)
            assert response.status_code == 401

    def test_put_task_invalid_data_response_400(self,api_client,common_user,common_task):
            task = common_task
            api_client.force_authenticate(user=common_user)
            url = reverse("todo:api-v1:tasks-detail",kwargs={"pk": task.pk},)
            data = {
                        "is_completed": False,
                    }
            response = api_client.put(url,data)
            assert response.status_code == 400

    def test_patch_task_response_200(self,api_client,common_user,common_task):
            task = common_task
            api_client.force_authenticate(user=common_user)
            url = reverse("todo:api-v1:tasks-detail",kwargs={"pk": task.pk},)
            data = {
                        "is_completed": False,
                    }
            response = api_client.patch(url,data)
            assert response.status_code == 200

    def test_patch_task_response_404(self,api_client,common_user):
                api_client.force_authenticate(user=common_user)
                url = reverse("todo:api-v1:tasks-detail",kwargs={"pk":259558123959416641541545455},)
                data = {
                            "is_completed": False,
                        }
                response = api_client.patch(url,data)
                assert response.status_code == 404

    def test_patch_task_response_401(self,api_client,common_task):
                task = common_task
                url = reverse("todo:api-v1:tasks-detail",kwargs={"pk": task.pk},)
                data = {
                        "is_completed": False,
                        }
                response = api_client.patch(url,data)
                assert response.status_code == 401

    def test_patch_task_invalid_data_response_400(self,api_client,common_user,common_task):
                task = common_task
                api_client.force_authenticate(user=common_user)
                url = reverse("todo:api-v1:tasks-detail",kwargs={"pk": task.pk},)
                data = {
                            "is_completed": 15,
                        }
                response = api_client.patch(url,data)
                assert response.status_code == 400

        
    
    

    
        
    