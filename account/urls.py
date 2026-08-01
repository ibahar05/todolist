from django.urls import path, include

from account import views

app_name="account"

urlpatterns = [
    path("login/",views.TodoLoginView.as_view(),name="login"),
    path("register/",views.TodoRegisterView.as_view(), name="register"),
    path("logout/",views.LogoutView.as_view(),name="logout"),
    path("api/v1/", include("account.api.v1.urls")),

]
