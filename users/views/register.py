from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from users.models import VerificationCode
from users.serializers.serializer import RegisterSerializer
from core.utilities.utils import generate_code, send_email_register_verification_code, logger
from django.db import transaction
from django_rq import enqueue

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        return self.register_without_organization(validated_data)

    def register_without_organization(self, validated_data):
        
        if User.objects.filter(email=validated_data["email"]).exists():
            return Response(
                {
                    "status": status.HTTP_406_NOT_ACCEPTABLE,
                    "message": "Similar Email already exists",
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        if validated_data["password1"] != validated_data["password2"]:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Passwords do not match",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, user_verification_code = self.create_user(validated_data)
        self.send_verification_email(user, user_verification_code)

        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "message": "Account registration is successful. Check your mail for verification code.",
            },
            status=status.HTTP_201_CREATED,
        )


    @transaction.atomic
    def create_user(self, validated_data):

        User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            password=validated_data["password1"],
            username=f"{validated_data['first_name']} {validated_data['last_name']}",
        )

        user = User.objects.filter(email=validated_data["email"]).first()
        logger.info(f"NEW USER: {user}")
        if user:
            if VerificationCode.objects.filter(user=user).exists():
                code = VerificationCode.objects.filter(user=user).first()
                logger.info(f"Deleting verification code {code.code}")

                VerificationCode.objects.filter(user=user).delete()
                logger.info("Deleted verification code")
        else:
            raise ValueError(
                "User object is None. Cannot create verification code without a user."
            )

        user_verification_code = VerificationCode.objects.create(
            user=user, code=generate_code()
        )

        return user, user_verification_code

    def send_verification_email(self, user, user_verification_code):

        try:
            send_email_register_verification_code(
                {
                    "email_to": user.email,
                    "greeting_to": user.username,
                    "verify_code": str(user_verification_code.code),
                }
            )
        except Exception as e:
            raise Exception(f"SMTP Error occurred: {str(e)}")