from django.urls import path, include

from . import views

app_name="api-v1"

urlpatterns = [
    path("register/",views.RegisterAPIView.as_view(), name="register"),
    path("activation/confrim/resend/",views.ResendActivationAPIView.as_view(),name="resend-activation"),
    path("activation/confirm/<str:token>/",views.ActivationAPIView.as_view(),name="activation"),

]
