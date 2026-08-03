from django.urls import path, include

from . import views

app_name="api-v1"

urlpatterns = [
    path("register/",views.RegisterAPIView.as_view(), name="register"),
    path("verification/resend/",views.ResendVerificationAPIView.as_view(),name="resend-activation"),
    path("verification/<str:token>/",views.VerificationAPIView.as_view(),name="activation"),
    path("change/password/",views.ChangePasswordAPIView.as_view(),name="change-password"),
]
