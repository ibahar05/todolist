from django.urls import path, include

from todo import views

app_name = "todo"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="todo"),
    path("task/create/", views.CreateTaskView.as_view(), name="create-task"),
    path("task/delete/<int:pk>/", views.DeleteTaskView.as_view(), name="delete-task"),
    path("task/update/<int:pk>/", views.UpdateTaskView.as_view(), name="update-task"),
    path("task/toggle<int:pk>/", views.ToggleTaskView.as_view(), name="task-toggle"),
    path("api/v1/", include("todo.api.v1.urls")),
]
