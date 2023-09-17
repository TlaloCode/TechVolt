import copy
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model, password_validation, user_logged_in
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import jwt
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from training_fyg.courses.models import Course, CourseInvitation, StudentCourse
from training_fyg.courses.serializers import StudentCourseSerializer
from training_fyg.users.models import (
    InvitationUsers,
    UserProfileRole,
    UserRegisterActivity,
)
from training_fyg.users.serializers.users import UserModelSerializer
from training_fyg.users.signals import get_client_ip
from training_fyg.users.tasks import (
    send_email_recovery,
    send_invitation_email,
    send_verify_account_email,
)
from training_fyg.users.utils import get_current_site_front

User = get_user_model()


class UserLoginTokenPairSerializer(TokenObtainSerializer):
    # noinspection PyMethodMayBeStatic
    def get_view_token(self, user, request):
        token = RefreshToken.for_user(user)
        # Agrega custom claims
        token["id"] = user.id
        token["username"] = user.username

        # Registra el acceso
        user_logged_in.send(sender=user.__class__, request=request, user=user)

        return token

    # noinspection PyMethodMayBeStatic
    def authenticate_user(self, request, username=None, password=None):
        if username is None or password is None:
            raise exceptions.AuthenticationFailed("Revise sus credenciales")

        user = User.objects.filter(email=username)
        if not user.exists():
            raise exceptions.AuthenticationFailed("No existe el usuario")
        user = user.first()

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Revise sus credenciales de inicio.")

        return user

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        user_id = attrs.get("user_id", None)
        if user_id:
            authenticate_kwargs.update({"user_id": attrs["user_id"]})

        request = self.context["request"]

        user = self.authenticate_user(request=request, **authenticate_kwargs)

        # no permite usuarios desactivados, pero sí los no verificados
        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                _("Oops... cuenta desactivada. Revisa tu correo.")
            )

        elif not user.is_verified:
            raise exceptions.AuthenticationFailed(
                "La cuenta no ha sido activada aún, revise su bandeja de correos e igual la carpeta de spam."
            )

        refresh = self.get_view_token(user, request)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserSignUpSerializer(serializers.Serializer):
    """User signup serializer.
    Clase para controlar el registro de usuarios del admin de training.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())], required=True
    )
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, max_length=64, required=True)
    password_confirmation = serializers.CharField(
        min_length=8, max_length=64, required=True
    )
    name = serializers.CharField(min_length=2, max_length=45, required=True)
    last_name = serializers.CharField(min_length=2, max_length=45)
    second_last_name = serializers.CharField(
        min_length=0, max_length=45, allow_blank=True, required=False
    )
    role = serializers.CharField(required=True, max_length=24)
    redirect_url = serializers.CharField(
        min_length=1,
        max_length=1000,
    )
    token = serializers.CharField(required=True)

    def validate(self, data):
        """Validación de contraseña."""
        password = data["password"]
        password_confirmation = data["password_confirmation"]

        if password != password_confirmation:
            raise serializers.ValidationError(
                {"password_confirmation": "Las contraseñas no coinciden"}
            )

        # Password valid or raise exception
        password_validation.validate_password(password)

        # revisar que exista un usuaro referenciado en el token y validar que sea una invitacion correcta
        try:
            payload = jwt.decode(
                data["token"], settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Link de verificación ha expirado")
        except jwt.exceptions.PyJWTError:
            raise serializers.ValidationError("Token inválido")

        user_request = User.objects.get(
            username=payload["user_request"], is_active=True
        )
        if data["role"] in ["ADMIN", "USER"] and user_request.role.value != "ADMIN":
            raise serializers.ValidationError(
                "El usuario anfitrión no tiene permisos para realizar esta invitación"
            )
        if data["role"] != payload["role"]:
            raise serializers.ValidationError(
                "El rol de usuario no coincide con el de la invitación"
            )

        return data

    def create(self, data):
        """Handle user and profile creation"""
        data.pop("password_confirmation")
        request = self.context.get("request")
        role = data.get("role")
        url = data.pop("redirect_url")

        role_obj = UserProfileRole.objects.get(value=role)

        data.pop("token")
        # Se usan estas _variables para crear el usuario sin modificar el data original
        _data = copy.deepcopy(data)
        _email = _data.pop("email")
        _name = _data.pop("name")
        _password = _data.pop("password")
        _last_name = _data.pop("last_name")

        user = User.objects.create_user(
            email=_email,
            password=_password,
            name=_name,
            last_name=_last_name,
            username=None,
            **_data
        )

        invitation = InvitationUsers.objects.get(email=_email)
        if invitation:
            invitation.user = user
            invitation.role = role_obj
            invitation.is_registered = True
            invitation.save()

        # Registra el registro
        user_agent_info = (request.META.get("HTTP_USER_AGENT", "<unknown>")[:255],)
        user_register_activity_log = UserRegisterActivity(
            register_IP=get_client_ip(request),
            register_username=user.username,
            register_email=user.email,
            register_rol=role_obj.pk,
            user_agent_info=user_agent_info,
            status=UserRegisterActivity.UserRegisterStatus.NO_VERIFIED,
        )
        user_register_activity_log.save()
        # manda email para verificación
        login_url = "{}{}".format(url, "auth/login")
        transaction.on_commit(
            lambda: send_verify_account_email.delay(
                user_pk=user.pk, full_path_domain=login_url
            )
        )

        return user


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Link de verificación ha expirado")
        except jwt.exceptions.PyJWTError:
            raise serializers.ValidationError("Token inválido")

        if payload["token_type"] != "email_confirmation":
            raise serializers.ValidationError({"token_type": "Token inválido"})

        self.context["payload"] = payload

        return data

    def save(self, **kwargs):
        """Update the user's verified active and status."""
        payload = self.context["payload"]
        user = User.objects.get(username=payload["user"])
        user.is_verified = True
        user.is_active = True
        user.save()

        pedings_courses = CourseInvitation.objects.filter(email=user.email)

        for pedings_course in pedings_courses:
            course = pedings_course.course_id
            StudentCourse.objects.create(
                user=user.id,
                course=course,
            )

        # Registra cambio de status
        if UserRegisterActivity.objects.filter(
            register_username=user.username
        ).exists():
            register_activity = UserRegisterActivity.objects.get(
                register_username=user.username
            )
            register_activity.status = UserRegisterActivity.UserRegisterStatus.VERIFIED
            register_activity.register_verified_datetime = timezone.now()
            register_activity.save()


class UserInvitationSerializer(serializers.Serializer):
    role = serializers.IntegerField()
    email = serializers.EmailField()


class ManagerInvitationSerializer(serializers.Serializer):
    """Manager invitation serializer."""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())], required=True
    )
    role = serializers.CharField(required=True, max_length=24)

    # noinspection PyMethodMayBeStatic
    def validate(self, attrs):
        if UserProfileRole.objects.filter(value=attrs["role"]).count() == 0:
            raise serializers.ValidationError({"role": "Rol inválido"})

        return attrs

    def save(self):
        """Handle user creation to send the email"""
        request = self.context["request"]
        user_request = request.user
        signup_url = "{}{}".format(get_current_site_front(), "/auth/signup")

        email = self.validated_data["email"]
        role = self.validated_data["role"]
        role_obj = UserProfileRole.objects.get(value=role)
        if InvitationUsers.objects.filter(email=email).exists():
            invitation = InvitationUsers.objects.get(email=email)
            invitation.count = invitation.count + 1
            invitation.role = role_obj
            invitation.send_at = datetime.now()
            invitation.save()
        else:
            InvitationUsers.objects.create(
                email=email, user=None, role=role_obj, send_at=datetime.now()
            )

        invitation = 0
        curso = 0
        transaction.on_commit(
            lambda: send_invitation_email(
                email=email,
                full_path_domain=signup_url,
                role=role,
                user_request=user_request.username,
                id_invitation=invitation,
                id_course=curso,
            )
        )


class InvitationUsersModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()

    class Meta:
        model = InvitationUsers
        fields = "__all__"


class StudentCourseInvitationSerializer(serializers.Serializer):
    """student course invitation serializer."""

    curso = serializers.IntegerField(required=True)

    email = serializers.EmailField(required=True)

    def save(self):
        email = self.validated_data["email"]
        curso = self.validated_data["curso"]

        if not Course.objects.filter(id=curso).exists():
            raise serializers.ValidationError({"course": "No existe curso"})
        else:
            nombrecurso = Course.objects.get(id=curso).name

        if not User.objects.filter(email=email).exists():
            role = "user"
            role_obj = UserProfileRole.objects.get(value=role)

            invitantion_exists = InvitationUsers.objects.filter(email=email).exists()
            if not invitantion_exists:
                InvitationUsers.objects.create(
                    email=email, user=None, role=role_obj, send_at=datetime.now()
                )

            if not CourseInvitation.objects.filter(
                email=email, course_id=curso
            ).exists():
                invitation = CourseInvitation.objects.create(
                    course_id=curso,
                    email=email,
                ).id
            else:
                invitation = CourseInvitation.objects.get(
                    email=email, course_id=curso
                ).id

            user_request = self.instance

            signup_url = "{}{}".format(get_current_site_front(), "/auth/signup")

            transaction.on_commit(
                lambda: send_invitation_email(
                    email=email,
                    full_path_domain=signup_url,
                    role="user",
                    user_request=user_request.user.username,
                    id_invitation=invitation,
                    id_course=curso,
                )
            )
        else:
            user_id = User.objects.get(email=email).id
            user_course = StudentCourse.objects.create(
                user=user_id,
                course=curso,
            )

            user_course = StudentCourseSerializer(user_course)
            data = user_course.data
            data["msg"] = "Usuario agregado correctamente a curso: " + nombrecurso


class PasswordRecoveryEmail(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        """if the email has an associated account send the recovery email."""
        email = data["email"]
        user = User.objects.filter(email=email)

        recovery_url = "{}{}".format(get_current_site_front(), "/resetear")

        if user.exists():
            transaction.on_commit(
                lambda: send_email_recovery(
                    user_pk=user[0].pk,
                    full_path_domain=recovery_url,
                )
            )
        else:
            raise serializers.ValidationError({"Error": "El Usuario no existe"})

        return data


class PasswordRecovery(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=64, required=True)
    password_confirmation = serializers.CharField(
        min_length=8, max_length=64, required=True
    )
    token = serializers.CharField(required=True)

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Link de verificación ha expirado")
        except jwt.exceptions.PyJWTError:
            raise serializers.ValidationError("Token inválido")

        if payload["token_type"] != "password_recovery":
            raise serializers.ValidationError({"token_type": "Token inválido"})

        self.context["payload"] = payload

        return data

    def validate(self, data):
        """Verifies passwords match."""
        password = data["password"]
        password_confirmation = data["password_confirmation"]
        token = data["token"]

        if password != password_confirmation:
            raise serializers.ValidationError(
                {"password_confirmation": "Las contraseñas no coinciden"}
            )

        # Password valid or raise exception
        password_validation.validate_password(password)
        self.validate_token(token)

        # Validate if exists the user
        try:
            User.objects.get(username=self.context["payload"]["user"])
        except User.DoesNotExist:
            raise serializers.ValidationError({"user": "Usuario no encontrado"})

        return data

    def save(self):
        user = User.objects.get(username=self.context["payload"]["user"])
        user.set_password(self.validated_data["password"])
        user.save()

        return user
