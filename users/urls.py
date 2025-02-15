from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from users.views import (
    login,
    register,
    confirm_register,
    register_resend_otp,
    change_password
)
from users.views import register

app_name = "users"

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("login/", view=login.LoginView.as_view(), name="login"),
    path("register/", view=register.RegisterView.as_view(), name="register"),
    path(
        "register/confirm/",
        view=confirm_register.ConfirmRegisterView.as_view(),
        name="register-confirm",
    ),
    # path(
    #     "password/send-otp/",
    #     view=send_otp_change_password.SendChangePasswordVerificationCodeView.as_view(),
    #     name="send-otp",
    # ),
    path(
        "register/resend-otp/",
        view=register_resend_otp.RegistrationConfirmResendOtp.as_view(),
        name="send-otp",
    ),
    # path(
    #     "password/forgot-password/",
    #     view=forget_password.ForgetPasswordView.as_view(),
    #     name="password-forgot",
    # ),
    # path(
    #     "password/confirm/forgot-password/",
    #     view=confirm_forget_password.ConfirmForgetPasswordView.as_view(),
    #     name="password-confirm",
    # ),
    path(
        "password/change/",
        view=change_password.ChangePasswordView.as_view(),
        name="password-change",
    ),
    # path("user/", view=user.UserDetailView.as_view(), name="user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=settings.DEBUG
)
urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=settings.DEBUG
)
