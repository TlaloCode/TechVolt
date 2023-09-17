import io
import logging
import random

from django.contrib.auth import get_user_model

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from training_fyg.courses.models import Course, CourseModule, Lesson

pytestmark = pytest.mark.django_db
LOG = logging.getLogger(__name__)


class SetupTest:
    def __init__(self):
        pass

    def create_ten_courses(self):
        names = ["curse " + str(num) for num in range(10)]

        courses = []
        for name in names:
            course = Course.objects.create(
                name=name,
                description=name * 3,
                course_type=random.choice(Course.CourseType.choices)[0],
            )
            courses.append(course)
            self.add_ten_modules_to_course(course=course)

        return courses

    def add_ten_modules_to_course(self, course):
        topics = [course.name + " topic " + str(num) for num in range(10)]

        modules = []
        for topic in topics:
            module = CourseModule.objects.create(
                course=course, topic=topic, description=topic * 3
            )
            modules.append(module)
            self.add_ten_lessons_to_module(module=module)

        return modules

    def add_ten_lessons_to_module(self, module):
        topics = [module.topic + " topic " + str(num) for num in range(10)]
        lessons = []

        for topic in topics:
            lesson = Lesson.objects.create(
                module=module, topic=topic, description=topic * 3, time_taken=10
            )
            lessons.append(lesson)

        return lessons

    def get_file_test(self):
        with open(".gitignore", "rb") as fp:
            fio = io.FileIO(fp.fileno())
            fio.name = "file.txt"
            r = self.client.post("/url/", {"filename": fio, "extraparameter": 5})
        self.assertEqual(r.headers["Content-Type"], "application/json")


class TestLesson(APITestCase, SetupTest):
    def setUp(self):
        self.courses = self.create_ten_courses()
        return None

    def get_admin_access(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username="admin",
            email="admin@admin.com",
            password="12345",
            name="Super",
            last_name="User Last Name",
        )
        self.client.force_authenticate(user=user)

    def test_list_lessons_module(self):
        self.get_admin_access()

        module = self.courses[0].modules.first()

        resp = self.client.get("/api/lessons/?module=" + str(module.id))

        self.assertEqual(resp.status_code, 200)

        assert "results" in resp.data

        assert isinstance(resp.data["results"], list)
        for lesson in resp.data["results"]:
            self.assertEqual(lesson["module"], module.id)

            assert "id" in lesson
            assert "topic" in lesson
            assert "description" in lesson

    def test_update_lesson(self):
        self.get_admin_access()

        lesson = Lesson.objects.first()

        old_topic = lesson.topic
        old_description = lesson.description

        topic = "new topic" + old_topic
        description = "new description" + old_description
        module = lesson.module.id
        time_taken = 15
        data = {
            "topic": topic,
            "description": description,
            "module": module,
            "time_taken": time_taken,
        }

        resp = self.client.put(f"/api/lessons/{lesson.id}/", data)
        lesson_updated = Lesson.objects.get(id=lesson.id)

        self.assertEqual(resp.status_code, 200)
        assert isinstance(resp.data, dict)
        assert "topic" in resp.data
        assert "description" in resp.data
        assert "time_taken" in resp.data
        self.assertEqual(resp.data["topic"], lesson_updated.topic, topic)
        self.assertEqual(
            resp.data["description"], lesson_updated.description, description
        )
        self.assertEqual(resp.data["time_taken"], lesson_updated.time_taken, time_taken)


class TestLessonViews:
    def test_create_new_lesson(
        self, api_client_with_user_credentials, create_user, fixture_module
    ):
        user = create_user()
        api_client = api_client_with_user_credentials(user=user)
        url = reverse("api:courses:courses:lessons-list")
        new_lesson = {
            "topic": "Mi lección",
            "description": "Descripción del módulo",
            "module": fixture_module(user=user).id,
            "time_taken": 5,
            "resources": [],
        }
        response = api_client.post(url, data=new_lesson, format="json")
        assert response.status_code == status.HTTP_201_CREATED
