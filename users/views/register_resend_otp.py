from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from core.utilities.utils import generate_code
from users.models import VerificationCode
from users.serializers.serializer import RegistrationConfirmResendOtpSerializer
from core.utilities.utils import (
    send_email_verification_code,
)

User = get_user_model()


class RegistrationConfirmResendOtp(generics.CreateAPIView):
    serializer_class = RegistrationConfirmResendOtpSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        data = RegistrationConfirmResendOtpSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        validated_data = data.data

        try:
            user = User.objects.filter(email=validated_data["email"]).first()
            if not user:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "message": "User not found",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            if user.is_verified:
                return Response(
                    {
                        "status": status.HTTP_406_NOT_ACCEPTABLE,
                        "message": f"User ({user}) already verified",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

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
                    "status": status.HTTP_201_CREATED,
                    "message": "Verification code sent. Check your mail.",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
