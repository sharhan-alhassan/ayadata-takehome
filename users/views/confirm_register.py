from datetime import timedelta
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from users.models import VerificationCode
from users.serializers.serializer import GeneralUserDetailsSerializer
from users.serializers.serializer import VerificationCodeSerializer


User = get_user_model()


class ConfirmRegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerificationCodeSerializer

    def post(self, request):
        try:
            data = VerificationCodeSerializer(data=request.data)
            data.is_valid(raise_exception=True)
            validated_data = data.data

            email = validated_data["email"]
            code = validated_data["code"]

            user = User.objects.filter(email=email).first()
            if not user:
                return Response(
                    {
                        "status": status.HTTP_406_NOT_ACCEPTABLE,
                        "message": "User does't exist!",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

            verify_code = VerificationCode.objects.filter(user=user, code=code).first()

            if verify_code:
                if verify_code.is_expired():
                    try:
                        verify_code.delete()
                    except:
                        pass
                    return Response(
                        {
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "The code has expired. Kindly request a new verification code",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if user.is_active == False:
                    user.is_active = True
                    user.is_verified = True
                    user.save()
                    # send_welcome_email_task.
                    try:
                        verify_code.delete()
                    except:
                        pass
                return Response(
                    {
                        "status": status.HTTP_200_OK,
                        "message": "Email verification successful",
                    },
                    status=status.HTTP_200_OK,
                )
            elif user.is_active == True:
                return Response(
                    {
                        "status": status.HTTP_200_OK,
                        "message": "Email already verified",
                    }
                )
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Verification code doesn't exist because it expired. Kindly request a new verification code",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except VerificationCode.DoesNotExist:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Invalid code provided",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
