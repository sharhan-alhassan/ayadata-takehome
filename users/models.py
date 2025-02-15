from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from users.base import BaseModel
from users.managers import CustomUserManager
from uuid import uuid4
from django.contrib.auth import get_user_model
from django.utils import timezone


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    username = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(_("Email Address"), unique=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.get_full_name()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        }


class VerificationCode(BaseModel):
    code = models.CharField(max_length=6, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    expires = models.DateTimeField()

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Verification Codes"

    def is_expired(self):
        return timezone.now() > self.expires

    @classmethod
    def get_default_expiry(cls):
        return timezone.now() + timezone.timedelta(hours=12)

    def save(self, *args, **kwargs):
        if not self.id:
            self.expires = self.get_default_expiry()
        super().save(*args, **kwargs)
