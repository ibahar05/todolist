from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "api-v1"
router = DefaultRouter()
router.register("tasks", views.TaskModelViewSet, basename="tasks")
urlpatterns = router.urls


# urlpatterns = [
#     # path("tasks/",views.tasklist,name="todo"),
#     # path("tasks/<id>",views.taskdetail, name="task-detail"),
#     path("tasks/",views.TaskList.as_view(),name="todo"),
#     path("tasks/<int:pk>",views.TaskDetail.as_view(), name="task-detail"),


# ]
