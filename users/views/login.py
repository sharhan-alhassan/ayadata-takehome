from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from users.models import VerificationCode
from users.serializers.serializer import LoginSerializer, UserLoginDetailSerializer
from core.utilities.utils import (
    generate_code,
    send_email_verification_code,
    logger
)

User = get_user_model()


class LoginView(generics.GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        data = LoginSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        validated_data = data.data

        user = User.objects.filter(email=validated_data["email"]).first()

        if user and not user.check_password(validated_data["password"]):
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Wrong password provided.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            if not user.is_active:
                if VerificationCode.objects.filter(user=user).exists():
                    VerificationCode.objects.get(user=user).delete()

                user_verification_code = VerificationCode.objects.create(
                    user=user, code=generate_code()
                )
                send_email_verification_code(
                    {
                        "email_to": user.email,
                        "verify_code": str(user_verification_code.code),
                    }
                )
                return Response(
                    {
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "message": "Email is not verified or account is inactive. Kindly check your email for a Token to verify first.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            data = {
                "status": status.HTTP_200_OK,
                "message": "Login successful",
                "tokens": user.tokens(),
                "data": UserLoginDetailSerializer(user).data,
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Wrong email, user does not exists",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
