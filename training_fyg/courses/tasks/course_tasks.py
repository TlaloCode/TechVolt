"""Celery auth users tasks."""
import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from config import celery_app

logger = logging.getLogger(__name__)


def get_site_back():
    return "localhost:8032"


@celery_app.task(name="send_email_message_training_sended", bind=True, max_retries=3)
def send_email_message_training_sended(
    self,
    email: str,
    full_path_domain: str,
    course_name: str,
    name: str,
):
    try:
        subject = f"El usuario { name } a colocado una nota del curso.!"

        site = Site.objects.get_current()

        headers = {}
        from_email = "Contacto FYG Training <contacto@framewarefactory.com>"
        headers.update({"Reply-To": settings.EMAIL_REPLY_TO})

        payload = {
            "full_path_domain": full_path_domain,
            "is_dev": settings.IS_DEV,
            "siteUrl": site,
            "course_name": course_name,
            "username": name,
        }
        content = render_to_string("emails/training_sended.html", payload)

        recipient_list = [
            email,
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
