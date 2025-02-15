
from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import VerificationCode

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    """Register User Serializer"""

    email = serializers.EmailField(max_length=100, min_length=4)
    first_name = serializers.CharField(max_length=170, min_length=3)
    last_name = serializers.CharField(max_length=170, min_length=3)
    password1 = serializers.CharField(
        min_length=6, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        min_length=6, required=True, style={"input_type": "password"}
    )
    
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6, required=True, style={"input_type": "password"}
    )
    email = serializers.EmailField(max_length=120, min_length=4)

    class Meta:
        model = User
        fields = ["email", "password"]
        
class UserLoginDetailSerializer(serializers.ModelSerializer):
    """User Details Serializer"""

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "username",
            "is_admin",
            "is_superuser",
            "is_active",
            "date_joined",
            "last_login",
        )
        read_only_fields = (
            "email",
            "is_admin",
            "last_login",
            "date_joined",
            "is_active",
        )
        
        
class GeneralUserDetailsSerializer(serializers.ModelSerializer):
    """General User Details Serializer"""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "is_active",
            "is_admin",
            "is_staff",
            "is_superuser",
        )
        read_only_fields = (
            "email",
            "last_login",
            "date_joined",
            "is_active",
            "is_staff",
        )
        
class VerificationCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=4)
    code = serializers.CharField(max_length=6, min_length=5)

    class Meta:
        model = VerificationCode
        fields = ["email", "code"]
        
        
class RegistrationConfirmResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    
class ChangePasswordConfirmSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        min_length=4, required=True, style={"input_type": "password"}
    )
    new_password1 = serializers.CharField(
        min_length=6, required=True, style={"input_type": "password"}
    )
    new_password2 = serializers.CharField(
        min_length=6, required=True, style={"input_type": "password"}
    )
    