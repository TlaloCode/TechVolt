"""Celery auth users tasks."""
import logging
from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

import jwt

from config import celery_app
from training_fyg.users.models import User

logger = logging.getLogger(__name__)


def get_site_back():
    return "localhost:8032"


def gen_verification_token(user: User, token_type="email_confirmation"):
    """Create JWT token that the user can use to verify its account."""
    exp_date = timezone.now() + timedelta(days=settings.JWT_TOKEN_EXP_DAYS)
    payload = {
        "user": user.username,
        "exp": int(exp_date.timestamp()),
        "token_type": token_type,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def gen_course_invitation_token(
    email: str, course: int, id_invitation: int, id_course: int
):
    """Create JWT token that the user can use to confirm."""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        "email": email,
        "course": course,
        "id_invitation": id_invitation,
        "id_course": id_course,
        "exp": int(exp_date.timestamp()),
        "token_type": "course_confirmation",
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def send_mail_from_invitation(
    verification_token: str,
    full_path_domain: str,
    email: str,
    subject: str,
):
    # site = Site.objects.get_current()
    site = get_site_back()

    # noinspection DuplicatedCode
    headers = {}

    from_email = "{} <{}>".format("Training", settings.EMAIL_HOST_USER)
    headers.update({"Reply-To": settings.EMAIL_REPLY_TO})

    # noinspection DuplicatedCode
    content = render_to_string(
        "emails/account_invitation.html",
        {
            "verification_token": verification_token,
            "full_path_domain": full_path_domain,
            "is_dev": settings.IS_DEV,
            "siteUrl": site,
        },
    )
    recipient_list = [
        email,
    ]

    email = EmailMultiAlternatives(
        subject=subject,
        body=content,
        from_email=from_email,
        to=recipient_list,
        headers=headers,
    )

    email.attach_alternative(content, "text/html")
    email.send()


def gen_manager_verification_token(
    email: str,
    role: str,
    user_request: str,
    id_invitation: int,
    id_course: int,
):
    """Create JWT token that the user can use to verify its account."""
    exp_date = timezone.now() + timedelta(days=settings.JWT_TOKEN_EXP_DAYS)
    payload = {
        "email": email,
        "user_request": user_request,
        "id_invitation": id_invitation,
        "id_course": id_course,
        "exp": int(exp_date.timestamp()),
        "token_type": "email_confirmation",
        "role": role,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


@celery_app.task(
    name="users_auth__send_manager_invitation_email", bind=True, max_retries=3
)
def send_invitation_email(
    self,
    email: str,
    full_path_domain: str,
    role: str,
    user_request: str,
    id_invitation: int,
    id_course: int,
):
    """Send email invitation link to new user."""
    try:
        verification_token = gen_manager_verification_token(
            email=email,
            role=role,
            user_request=user_request,
            id_invitation=id_invitation,
            id_course=id_course,
        )
        subject = "Has recibido una invitación para unirte a Training FyG"
        if role == "admin":
            subject = "Has recibido una invitación para administrar Training FyG"

        send_mail_from_invitation(
            verification_token,
            full_path_domain,
            email,
            subject,
        )
    except Exception as ex:
        logger.exception(ex)
        self.retry(countdown=3**self.request.retries)


@celery_app.task(name="users_auth__send_verify_account_email", bind=True, max_retries=3)
def send_verify_account_email(self, user_pk: int, full_path_domain: str):
    """Envia el email de verificacion a un adminsitrador de tienda."""
    try:
        user = User.objects.get(pk=user_pk)
        # site = Site.objects.get_current()
        site = get_site_back()
        verification_token = gen_verification_token(user)
        subject = (
            "¡Bienvenido @{}! Verifica tu cuenta para comenzar a usar Training".format(
                user.name
            )
        )
        from_email = "Contacto {} <{}>".format("Training", "contacto@trainingfyg.com")
        headers = {"Reply-To": settings.EMAIL_REPLY_TO}

        content = render_to_string(
            "emails/account_verification.html",
            {
                "full_path_domain": full_path_domain,
                "verification_token": verification_token,
                "user": user,
                "is_dev": settings.IS_DEV,
                "siteUrl": site,
            },
        )
        recipient_list = [
            user.email,
        ]

        msg = EmailMultiAlternatives(
            subject=subject,
            body=content,
            from_email=from_email,
            to=recipient_list,
            headers=headers,
        )
        msg.attach_alternative(content, "text/html")
        msg.send()

    except Exception as ex:
        logger.exception(ex)
        self.retry(countdown=3**self.request.retries)


@celery_app.task(name="users_auth__send_course_email", bind=True, max_retries=3)
def send_course_invitation(
    self,
    email: str,
    course: str,
    full_path_domain: str,
    user_request: str,
    id_invitation: int,
    id_course: int,
):
    try:
        verification_token = gen_course_invitation_token(
            email=email, course=course, id_invitation=id_invitation, id_course=id_course
        )
        # signup_url = f"{full_site_url}{urls.get('signup')}"
        # full_path_domain = Site.objects.get_current().domain
        subject = f"Has recibido una invitación para unirte al curso {course} en Train"
        recipient_list = [email]
        headers = {"Reply-To": settings.EMAIL_REPLY_TO}
        from_email = "Contacto {} <{}>".format("Training", "contacto@training.com")

        content = render_to_string(
            "emails/course.html",
            {
                "full_path_domain": full_path_domain,
                "verification_token": verification_token,
                "is_dev": settings.IS_DEV,
                "course": course,
            },
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=content,
            from_email=from_email,
            to=recipient_list,
            headers=headers,
        )
        msg.attach_alternative(content, "text/html")
        msg.send()

    except Exception:
        self.retry(countdown=3**self.request.retries)


@celery_app.task(name="users_auth__send_email_recovery", bind=True, max_retries=3)
def send_email_recovery(self, user_pk: int, full_path_domain: str):
    """Send the email password recovery."""
    try:
        # full_site_url = Site.objects.get_current().domain
        user = User.objects.get(pk=user_pk)
        full_path_domain = f"{full_path_domain}"
        verification_token = gen_verification_token(user, "password_recovery")

        subject = f"{user.name}, Has recibido una invitación para restaurar tu password en Train"
        recipient_list = [user.email]
        headers = {"Reply-To": settings.EMAIL_REPLY_TO}
        from_email = "Contacto {} <{}>".format("Training", "contacto@training.com")
        content = render_to_string(
            "emails/account_recovery.html",
            {
                "full_path_domain": full_path_domain,
                "verification_token": verification_token,
                "user": user,
            },
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=content,
            from_email=from_email,
            to=recipient_list,
            headers=headers,
        )
        msg.attach_alternative(content, "text/html")
        msg.send()

    except Exception as ex:
        logger.exception(ex)
        self.retry(countdown=3**self.request.retries)
