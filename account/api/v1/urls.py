from django.urls import path, include
from rest_framework_simplejwt.views import (TokenRefreshView,
                                            TokenVerifyView)

from . import views

app_name="api-v1"

urlpatterns = [
    path("register/",views.RegisterAPIView.as_view(), name="register"),
    path("verification/resend/",views.ResendVerificationAPIView.as_view(),name="resend-activation"),
    path("verification/<str:token>/",views.VerificationAPIView.as_view(),name="activation"),
    path("change/password/",views.ChangePasswordAPIView.as_view(),name="change-password"),

    path("jwt/create/", views.CustomObtainPairView.as_view(),name="jwt-create"),
    path("jwt/refresh/",TokenRefreshView.as_view(),name = "jwt-refresh"),
    path("jwt/verify/",TokenVerifyView.as_view(),name = "jwt-verify"),

]
