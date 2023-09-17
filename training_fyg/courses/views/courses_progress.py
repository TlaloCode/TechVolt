from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet

from training_fyg.courses.models import Course
from training_fyg.courses.serializers import CourseLessonProgressModelSerializer


class CourseLessonProgressViewSet(ModelViewSet):
    serializer_class = CourseLessonProgressModelSerializer
    queryset = CourseLessonProgressModelSerializer.Meta.model.objects.filter(
        is_active=True
    )

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]

        return (permission() for permission in permissions)

    @action(
        detail=False,
        methods=[
            "POST",
        ],
        url_name="generate-progress",
        url_path="generate-progress",
    )
    def generate_progress(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(
        detail=True,
        methods=[
            "GET",
        ],
        url_name="lessons-progress",
        url_path="lessons-progress",
    )
    def lessons_progress(self, request, *args, **kwargs):
        # Obtiene el curso sobre el que se obtendrán las lecciones
        self.queryset = Course.objects.filter(is_active=True).order_by("id")
        obj_course = self.get_object()
        # Obtiene la lista de lecciones, actualizando el queryset
        self.serializer_class = CourseLessonProgressModelSerializer
        self.queryset = CourseLessonProgressModelSerializer.Meta.model.objects.filter(
            is_active=True, lesson__module__course_id=obj_course.id
        ).order_by("id")
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # noinspection PyMethodMayBeStatic
    def perform_create(self, serializer):
        serializer.save()

    # noinspection PyMethodMayBeStatic
    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
