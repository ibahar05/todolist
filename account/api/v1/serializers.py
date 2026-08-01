from rest_framework import serializers
from ...models import User 
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id","email","password","password1"]


    def validate(self,attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail":"passwords don't match"})
        
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"error":list(e.messages)})
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop("password1",None)
        return User.objects.create_user(**validated_data)


class ResendActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError({"detail":"User does not exist"})
        if user_obj.is_verified:
            raise serializers.ValidationError({"detail":"User is verified already"})
        attrs["user_obj"] = user_obj
        return super().validate(attrs)
        
        