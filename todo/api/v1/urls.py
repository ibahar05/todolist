from django.urls import path, include

from . import views

app_name="api-v1"

urlpatterns = [
    # path("tasks/",views.tasklist,name="todo"),
    # path("tasks/<id>",views.taskdetail, name="task-detail"),
    path("tasks/",views.TaskList.as_view(),name="todo"),
    path("tasks/<int:id>",views.TaskDetail.as_view(), name="task-detail"),


]
