import logging

from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db
User = get_user_model()
logger = logging.getLogger(__name__)


class TestCourse:
    def test_create_new_course(self, api_client_with_user_credentials):
        url = reverse("api:courses:courses:courses-list")
        new_course = {
            "image": None,
            "name": "Prueba curso",
            "categories": [],
            "courseType": "public",
            "description": "Descripción del curso",
            "modules": [],
        }
        response = api_client_with_user_credentials().post(
            url, data=new_course, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
