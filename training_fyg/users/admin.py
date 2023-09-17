"""User models admin."""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from training_fyg.users.forms import UserChangeForm, UserCreationForm
from training_fyg.users.models.auth import UserLoginActivity, UserRegisterActivity

# Models
from training_fyg.users.models.users import InvitationUsers

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "name",
                    "last_name",
                    "second_last_name",
                    "phone_number",
                    "email",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_verified",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "role",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = [
        "id",
        "username",
        "name",
        "last_name",
        "email",
        "role",
        "is_active",
        "is_verified",
        "is_superuser",
    ]
    list_editable = (
        "name",
        "email",
        "last_name",
        "is_active",
        "is_verified",
    )
    list_select_related = ("role",)
    search_fields = ["name", "username", "email"]


@admin.register(UserLoginActivity)
class UserLoginActivityModelAdmin(admin.ModelAdmin):
    """UserLoginActivity model admin."""

    list_display = (
        "id",
        "login_username",
        "login_IP",
        "status",
        "login_datetime",
        "user_agent_info",
    )
    list_display_links = (
        "id",
        "login_username",
    )


@admin.register(UserRegisterActivity)
class UserRegisterActivityModelAdmin(admin.ModelAdmin):
    """UserRegisterActivity model admin."""

    list_display = (
        "id",
        "register_username",
        "register_email",
        "register_IP",
        "status",
        "register_datetime",
        "register_verified_datetime",
        "user_agent_info",
    )
    list_display_links = (
        "id",
        "register_username",
    )


@admin.register(InvitationUsers)
class UserInvitationModelAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = (
        "email",
        "count",
        "user",
        "is_registered",
        "send_at",
        "created_at",
        "modified_at",
    )
    list_display_links = ("email",)
