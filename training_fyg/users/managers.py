from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

from training_fyg.users.utils import generate_username


class CustomUserManager(BaseUserManager):
    def _create_user(
        self,
        email: str,
        password: str,
        name: str,
        last_name: str,
        username=None,
        **extra_fields
    ):
        """
        Creates and saves a User with the given email, password, name and last_name.
        """
        if not email:
            raise ValueError("The given email must be set")
        if not password:
            raise ValueError("The given password must be set")
        if not name:
            raise ValueError("The given name must be set")
        if not last_name:
            raise ValueError("The given last_name must be set")

        email = self.normalize_email(email)
        if username is None:
            username = generate_username(name, last_name)

        if extra_fields.get("role") is not None:
            # noinspection PyPep8Naming
            RoleModel = apps.get_model("users", "UserProfileRole")
            role = extra_fields.pop("role")
            extra_fields.setdefault("role", RoleModel.objects.get(value=role))

        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        # noinspection PyPep8Naming,PyProtectedMember
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("role", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_verified") is not True:
            raise ValueError("Superuser must have is_verified=True.")
        if extra_fields.get("name") is None:
            raise ValueError("Superuser must have name.")
        if extra_fields.get("last_name") is None:
            raise ValueError("Superuser must have last_name.")
        name = extra_fields.pop("name")
        last_name = extra_fields.pop("last_name")

        return self._create_user(
            email, password, name, last_name, username, **extra_fields
        )

    def create_user(
        self,
        email,
        password=None,
        name=None,
        last_name=None,
        username=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            email, password, name, last_name, username, **extra_fields
        )

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()
