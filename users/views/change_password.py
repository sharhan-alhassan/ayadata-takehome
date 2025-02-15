from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from users.serializers.serializer import ChangePasswordConfirmSerializer

User = get_user_model()

class ChangePasswordView(generics.CreateAPIView):
    serializer_class = ChangePasswordConfirmSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data["old_password"]
        new_password1 = serializer.validated_data["new_password1"]
        new_password2 = serializer.validated_data["new_password2"]

        if not check_password(old_password, user.password):
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST, 
                    "message": "Old password is incorrect."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_password1 != new_password2:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST, 
                    "message": "New passwords do not match."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password1)
        user.save()

        return Response(
            {
                "status": status.HTTP_200_OK, 
                "message": "Password changed successfully."
            },
            status=status.HTTP_200_OK,
        )
