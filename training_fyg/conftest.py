import pytest
from faker import Faker
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from training_fyg.categories.models import CategoryCourse
from training_fyg.courses.models import Course, CourseModule, HomeworkLesson, Lesson
from training_fyg.users.models import User, UserProfileRole
from training_fyg.users.tests.factories import UserFactory

fake = Faker("es_MX")


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def api_public_client() -> APIClient:
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(role="USER") -> User:
        username = fake.user_name()
        email = fake.email()
        first_name = fake.first_name()
        last_name = fake.last_name()
        password = User.objects.make_random_password()
        role_obj = UserProfileRole.objects.get(value=role)
        user = User.objects.create(
            name=first_name,
            last_name=last_name,
            email=email,
            role=role_obj,
            username=username,
            password=password,
            is_active=True,
            is_verified=True,
            is_staff=False,
            is_superuser=False,
        )
        return user

    return make_user


@pytest.fixture
def fixture_category(db, create_user) -> CategoryCourse:
    user = create_user()
    return CategoryCourse.objects.create(name="my_course", created_by=user)


@pytest.fixture
def fixture_course(db, create_user, fixture_category):
    def make_course(user: User = None) -> Course:
        if user is None:
            user = create_user()
        course = Course.objects.create(
            name="my_course",
            description="Test course description",
            course_type=Course.CourseType.PUBLIC,
            created_by=user,
        )
        course.categories.set([fixture_category.id])
        course.save()
        return course

    return make_course


@pytest.fixture
def fixture_module(db, fixture_course):
    def make_module(user: User = None) -> CourseModule:
        course = fixture_course(user=user)
        user = course.created_by
        return CourseModule.objects.create(
            course=course,
            topic="Module topic",
            description="Module description",
            created_by=user,
        )

    return make_module


@pytest.fixture
def fixture_lesson(db, fixture_module):
    def make_lesson(user: User = None) -> Lesson:
        module = fixture_module(user=user)
        user = module.created_by
        return Lesson.objects.create(
            module=module,
            topic="Lesson topic",
            description="Module description",
            created_by=user,
        )

    return make_lesson


@pytest.fixture
def fixture_homework(db, fixture_lesson):
    def make_homework(user: User = None) -> HomeworkLesson:
        lesson = fixture_lesson(user=user)
        user = lesson.created_by
        return HomeworkLesson.objects.create(
            lesson=lesson,
            title="Homework title",
            description="Homework description",
            created_by=user,
        )

    return make_homework


@pytest.fixture
def create_token(db, create_user):
    def make_token(user: User = None, role="USER"):
        if user is None:
            user = create_user(role=role)
        token = RefreshToken.for_user(user)
        token["id"] = user.id
        token["username"] = user.username
        return str(token.access_token)

    return make_token


@pytest.fixture
def api_client_with_admin_credentials(api_public_client, create_token):
    def make_api_client(user: User = None) -> APIClient:
        token = create_token(user=user, role="ADMIN")
        api_public_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        return api_public_client

    return make_api_client


@pytest.fixture
def api_client_with_user_credentials(api_public_client, create_token):
    def make_api_client(user: User = None) -> APIClient:
        token = create_token(user=user, role="USER")
        api_public_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        return api_public_client

    return make_api_client
