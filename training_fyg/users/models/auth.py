from django.db import models


class UserLoginActivity(models.Model):
    class UserLoginActivityStatus(models.TextChoices):
        SUCCESS = "S", "Exitoso"
        FAILED = "F", "Fallido"

    login_IP = models.GenericIPAddressField(
        verbose_name="Ip de login", null=True, blank=True
    )
    login_datetime = models.DateTimeField(
        verbose_name="Fecha y hora de login", auto_now=True
    )
    login_username = models.CharField(
        verbose_name="Login username", max_length=40, null=True, blank=True
    )
    status = models.CharField(
        verbose_name="Estatus",
        max_length=1,
        default=UserLoginActivityStatus.SUCCESS,
        choices=UserLoginActivityStatus.choices,
        null=True,
        blank=True,
    )
    user_agent_info = models.CharField(
        verbose_name="Información del agente de usuario", max_length=255
    )

    def __str__(self):
        """Return user's str representation."""
        return "{} - {}".format(self.login_username, self.login_datetime)

    class Meta:
        verbose_name = "Actividad de login de usuario"
        verbose_name_plural = "Actividades de login de usuarios"


class UserRegisterActivity(models.Model):
    class UserRegisterStatus(models.TextChoices):
        VERIFIED = "V", "Verificado"
        NO_VERIFIED = "SV", "Sin Verificado"

    register_IP = models.GenericIPAddressField(
        verbose_name="Ip de registro", null=True, blank=True
    )
    register_datetime = models.DateTimeField(
        verbose_name="Fecha y hora de registro",
        auto_now_add=True,
    )
    register_verified_datetime = models.DateTimeField(
        verbose_name="Fecha y hora de registro verificado", null=True, blank=True
    )
    register_username = models.CharField(
        verbose_name="registro username", max_length=40, null=True, blank=True
    )
    register_email = models.CharField(
        verbose_name="registro email", max_length=40, null=True, blank=True
    )
    register_rol = models.CharField(
        verbose_name="registro rol del usuario", max_length=40, null=True, blank=True
    )
    status = models.CharField(
        verbose_name="Estatus",
        max_length=2,
        default=UserRegisterStatus.NO_VERIFIED,
        choices=UserRegisterStatus.choices,
        null=True,
        blank=True,
    )
    user_agent_info = models.CharField(
        verbose_name="Información del agente de usuario", max_length=255
    )

    def __str__(self):
        """Return user's str representation."""
        return "{} - {}".format(self.register_username, self.register_datetime)

    class Meta:
        verbose_name = "Actividad de registro de usuario"
        verbose_name_plural = "Actividades de registro de usuarios"
