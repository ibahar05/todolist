from django.urls import path, include

from . import views

app_name="api-v1"

urlpatterns = [
    path("tasks/",views.postlist,name="todo"),

]
