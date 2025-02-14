from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, **extra_fields):
        if not email and "@" not in email:
            raise ValueError(_("The Email must be set"))

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user = user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        if not email and "@" not in email:
            raise ValueError(_("The Email must be set"))

        email = self.normalize_email(email)
        super_user = self.model(email=email, **extra_fields)
        super_user.set_password(password)

        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.is_active = True
        super_user.is_admin = True
        return super_user.save()
