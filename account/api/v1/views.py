from rest_framework.response import Response
from rest_framework import generics
from .serializers import (
    RegisterSerializer,
    ResendVerificationSerializer,
    ChangePasswordSerializer,
    CustomObtainPairSerializer,
)
from django.shortcuts import get_object_or_404
from ...models import User
from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage
from ..utils import EmailThreading
from rest_framework import status
from rest_framework.views import APIView
import jwt
from django.conf import settings
from jwt import ExpiredSignatureError, InvalidSignatureError
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            user_obj = get_object_or_404(User, email=email)
            token = self.get_token_for_users(user_obj)
            email_obj = EmailMessage(
                "email/verification_email.tpl",
                {"token": token},
                "admin@admin.com",
                to=[email],
            )
            EmailThreading(email_obj).start()
            return Response(
                {"detail": "Account created"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_token_for_users(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class VerificationAPIView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"detail": "token is expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "token is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response(
                {"detail": "your account is verified already"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"detail": "your account verified successfilly"}, status=status.HTTP_200_OK
        )


class ResendVerificationAPIView(generics.GenericAPIView):
    serializer_class = ResendVerificationSerializer

    def post(self, reauest, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user_obj"]
        token = self.get_token_for_users(user_obj)
        email_obj = EmailMessage(
            "email/verification_email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThreading(email_obj).start()
        return Response(
            {"detail": "Verification Resend"}, status=status.HTTP_201_CREATED
        )

    def get_token_for_users(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"detial": "wrong password"})
            user.set_password(serializer.validated_data["new_password1"])
            user.save()
            return Response(
                {"detail": "Password changed successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainPairView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer
