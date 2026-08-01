from rest_framework.response import Response
from rest_framework import generics
from .serializers import RegisterSerializer,ResendActivationSerializer
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

class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            user_obj = get_object_or_404(User, email=email)
            token = self.get_token_for_users(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, "admin@admin.com",
                       to=[email])
            EmailThreading(email_obj).start()
            return Response({"detail":"Account created"}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_token_for_users(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

class ActivationAPIView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY,algorithms=["HS256"])
            user_id = decoded_token.get("user_id")
        except ExpiredSignatureError:
            return Response({"detail":"token is expired"},status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({"detail":"token is invalid"},status=status.HTTP_400_BAD_REQUEST)

        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({"detail":"Your account has been verified successfully"},status=status.HTTP_400_BAD_REQUEST)

        user_obj.is_verified = True
        user_obj.save()
        return Response({"detail":"Your account is verified now"},status=status.HTTP_200_OK)
    

class ResendActivationAPIView(generics.GenericAPIView):
    serializer_class = ResendActivationSerializer

    def post(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user_obj"]
        token = self.get_token_for_users(user_obj)
        email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, "admin@admin.com",to=[user_obj.email])
        EmailThreading(email_obj).start()
        return Response({"detail":"Activation Resend"}, status = status.HTTP_200_OK)

    def get_token_for_users(self, user):
            refresh = RefreshToken.for_user(user)
            return str(refresh.access_token)
