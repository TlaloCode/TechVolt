import logging

from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework import status

from training_fyg.courses.models import TeacherCourse

pytestmark = pytest.mark.django_db
User = get_user_model()

LOG = logging.getLogger(__name__)


class TestHomeworkViews:
    def test_create_new_homework(
        self, api_client_with_user_credentials, create_user, fixture_lesson
    ):
        user = create_user()
        api_client = api_client_with_user_credentials(user=user)
        url = reverse("api:courses:courses:homework-lesson-list")
        new_homework = {
            "title": "Mi tarea",
            "description": "Descripción de la tarea",
            "lesson": fixture_lesson(user=user).id,
            "resources": [],
        }
        response = api_client.post(url, data=new_homework, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_duplicated_homework(
        self, api_client_with_user_credentials, create_user, fixture_lesson
    ):
        user = create_user()
        lesson = fixture_lesson(user=user)
        api_client = api_client_with_user_credentials(user=user)
        url = reverse("api:courses:courses:homework-lesson-list")
        new_homework = {
            "title": "Mi tarea",
            "description": "Descripción de la tarea",
            "lesson": lesson.id,
            "resources": [],
        }
        api_client.post(url, data=new_homework, format="json")
        response = api_client.post(url, data=new_homework, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_permission_delete_homework_ok(
        self, api_client_with_user_credentials, create_user, fixture_homework
    ):
        """Verifica que un usuario pueda eliminar una tarea propia"""
        user = create_user()

        api_client = api_client_with_user_credentials(user=user)
        homework = fixture_homework(user=user)
        # Genera la relación entre el profesor y el curso
        TeacherCourse.objects.create(user=user, course=homework.lesson.module.course)
        url = reverse(
            "api:courses:courses:homework-lesson-detail", kwargs={"pk": homework.id}
        )
        response = api_client.delete(url)
        LOG.info(response.__dict__)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_permission_delete_homework_not_allowed(
        self, api_client_with_user_credentials, fixture_homework
    ):
        """Intenta eliminar la tarea de una lección al que no pertenece el usuario"""
        # Al no enviar el usuario al método fixture_homework, se estará generando un nuevo usuario
        homework = fixture_homework()
        api_client = api_client_with_user_credentials()
        url = reverse(
            "api:courses:courses:homework-lesson-detail", kwargs={"pk": homework.id}
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
