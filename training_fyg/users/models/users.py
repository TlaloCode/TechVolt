"""User model."""

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from training_fyg.users.managers import CustomUserManager
from training_fyg.utils.models import BaseModel, CustomAbstractUser


class UserProfileRole(models.Model):
    """
    UserProfileRole.
    Table with available roles.
    """

    alphanumeric = RegexValidator(
        r"^[A-Z_]*$", "Sólo se permiten mayusculas y guiones bajos."
    )

    value = models.CharField(
        verbose_name="Rol",
        validators=[alphanumeric],
        unique=True,
        max_length=24,
        primary_key=True,
    )

    title = models.CharField(
        verbose_name="Rol",
        unique=True,
        max_length=24,
    )

    created_at = models.DateTimeField(
        verbose_name="Fecha de creación",
        auto_now_add=True,
        help_text="Fecha en que el registro fue creado.",
    )
    modified_at = models.DateTimeField(
        verbose_name="Ultima modificación",
        auto_now=True,
        help_text="Última fecha en que el registro fue modificado",
    )

    class Meta:
        verbose_name = "Rol de usuario"
        verbose_name_plural = "Roles de usuarios"

    def __str__(self):
        """Return role."""
        return self.title


class User(BaseModel, CustomAbstractUser):
    """User model.
    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    picture = models.ImageField(  # noqa DJ01
        verbose_name="Avatar",
        upload_to="users/profiles/user-profile/picture/%Y/%m/%d/",
        max_length=1000,
        blank=True,
        null=True,
    )
    role = models.ForeignKey(
        verbose_name="Rol de usuario",
        on_delete=models.CASCADE,
        to="users.UserProfileRole",
        default="USER",
    )
    email = models.EmailField(
        "email address",
        error_messages={"unique": "A user with that email already exists."},
    )

    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed.",
    )

    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Indica si el registro debe ser tratado como activo. Desmarque esta opción en lugar de borrar el registro",
        ),
    )
    is_verified = models.BooleanField(
        "verified",
        default=False,
        help_text="Set to true when the user have verified its email address.",
    )
    created_by = models.ForeignKey(
        verbose_name="Usuario creador",
        to="users.User",
        on_delete=models.CASCADE,
        null=True,
        related_name="%(app_label)s_%(class)s_created",
    )
    modified_by = models.ForeignKey(
        verbose_name="Usuario editor",
        to="users.User",
        on_delete=models.CASCADE,
        null=True,
        related_name="%(app_label)s_%(class)s_modified",
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name", "last_name"]
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        """Return username."""
        return self.username


class InvitationUsers(models.Model):
    """
    InvitationUsers.
    Table with invitations.
    """

    email = models.EmailField(
        verbose_name="email address",
        error_messages={"unique": "A user with that email already exists."},
    )
    count = models.IntegerField(verbose_name="Contador de envios", default=1)
    user = models.ForeignKey(
        verbose_name="usuario", on_delete=models.CASCADE, to="users.User", null=True
    )
    role = models.ForeignKey(
        verbose_name="Rol de usuario",
        on_delete=models.CASCADE,
        to="users.UserProfileRole",
        default="USER",
    )
    is_registered = models.BooleanField(
        verbose_name="registrado",
        default=False,
        help_text="Indica si la invitacion fue resuelta.",
    )
    send_at = models.DateTimeField(
        verbose_name="Fecha de ultima invitacion",
        help_text="Fecha en que se mando por ultima vez el correo.",
    )
    created_at = models.DateTimeField(
        verbose_name="Fecha de creación",
        auto_now_add=True,
        help_text="Fecha en que el registro fue creado.",
    )
    modified_at = models.DateTimeField(
        verbose_name="Ultima modificación",
        auto_now=True,
        help_text="Última fecha en que el registro fue modificado",
    )

    class Meta:
        verbose_name = "Invitación a usuario"
        verbose_name_plural = "Invitaciones a usuarios"

    def __str__(self):
        """Return role."""
        return self.email
