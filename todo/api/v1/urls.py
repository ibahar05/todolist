from django.urls import path, include

from . import views

app_name="api-v1"

urlpatterns = [
    path("tasks/",views.tasklist,name="todo"),
    path("tasks/<id>",views.taskdetail, name="task-detail"),

]
