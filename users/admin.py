# Python/Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from users.models import CustomUser
from users.models import VerificationCode
from django.contrib import admin

admin.site.site_header = "Ayadata Admin"
admin.site.site_title = "Ayadata Admin"


class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserAdmin(UserAdmin):
    form = CustomUserAdminForm

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "username", "avatar")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_verified",
                    "is_admin",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not obj:
            if len(fieldsets) > 2:
                fieldsets[2][1]["fields"] = (
                    "is_active",
                    "is_verified",
                    "is_staff",
                    "is_superuser",
                    "is_admin",
                )
        return fieldsets

    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "username",
        "is_staff",
        "is_active",
        "is_verified",
        "is_admin",
    )
    list_filter = (
        "first_name",
        "last_name",
        "username",
        "email",
        "is_staff",
        "is_active",
    )
    search_fields = (
        "email",
        "username",
    )
    ordering = (
        "email",
        "username",
    )
    readonly_fields = ("date_joined", "last_login")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(VerificationCode)
