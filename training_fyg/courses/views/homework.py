import logging

from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions, mixins, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from url_filter.integrations.drf import DjangoFilterBackend

from training_fyg.courses.models import (
    HomeworkLesson,
    HomeworkLessonDelivery,
    HomeworkLessonResource,
    HomeworkLessonReview,
)
from training_fyg.courses.permissions import IsCourseOwner
from training_fyg.courses.serializers import (
    HomeworkLessonDeliverySerializer,
    HomeworkLessonModelSerializer,
    HomeworkLessonResourceModelSerializer,
    HomeworkLessonReviewSerializer,
)
from training_fyg.users.permissions.users import IsAdminPermission
from training_fyg.utils.custom_mixins.mixins_serializers import (
    CustomCreateModelMixin,
    CustomModelViewSet,
)

logger = logging.getLogger("console")


class HomeworkLessonViewSet(CustomModelViewSet):
    queryset = (
        HomeworkLesson.objects.select_related("lesson")
        .prefetch_related("homeworklessonresource")
        .filter(is_active=True)
    )
    serializer_class = HomeworkLessonModelSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = [
        "lesson",
    ]

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ["destroy", "update"]:
            permissions = [IsAuthenticated, IsCourseOwner | IsAdminPermission]
        else:
            permissions = [IsAuthenticated]

        return (permission() for permission in permissions)

    def perform_destroy(self, instance):
        # Valida si la tarea tiene tareas entregadas
        if (
            HomeworkLessonDelivery.objects.filter(
                is_active=True, homework_lesson_id__in=[instance.id]
            ).count()
            > 0
        ):
            raise serializers.ValidationError(
                {"homework": _("No se pueden eliminar la tarea con entregas activas")}
            )

        instance.is_active = False
        instance.save()

    @action(methods=["GET"], detail=True, url_name="messages", url_path="messages")
    def get_messages(self, request, *args, **kwargs):
        homework = self.get_object()
        query = HomeworkLessonDeliverySerializer.Meta.model.objects.filter(
            homework_lesson__id=homework.id
        )
        serializer = HomeworkLessonDeliverySerializer(query, many=True)
        return Response(serializer.data)


class HomeworkLessonDeliveryViewSet(CustomModelViewSet):
    queryset = (
        HomeworkLessonDelivery.objects.select_related("created_by")
        .select_related("homework_lesson")
        .select_related("homework_lesson__lesson")
        .select_related("homework_lesson__lesson__module")
        .select_related("homework_lesson__lesson__module__course")
        .prefetch_related("homework_lesson__homeworklessonresource")
        .filter(is_active=True)
    )
    serializer_class = HomeworkLessonDeliverySerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = [
        "created_by",
    ]

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [
            IsAuthenticated,
        ]

        return (permission() for permission in permissions)


class HomeworkLessonReviewViewSet(CustomModelViewSet):
    queryset = HomeworkLessonReview.objects.filter(is_active=True)
    serializer_class = HomeworkLessonReviewSerializer
    filter_fields = [
        "homework_lesson_delivery__id",
    ]

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [
            IsAuthenticated,
        ]

        return (permission() for permission in permissions)

    def get_serializer_class(self):
        if self.action == "partial_update":
            raise exceptions.MethodNotAllowed(self.request.method)
        return super(HomeworkLessonReviewViewSet, self).get_serializer_class()


class HomeworkLessonResourceViewSet(
    viewsets.GenericViewSet,
    CustomCreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    queryset = HomeworkLessonResource.objects.filter(is_active=True)
    serializer_class = HomeworkLessonResourceModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]

        return (permission() for permission in permissions)

    def get_queryset(self):
        homework_lesson_id = self.request.query_params.get("homeworkLesson", None)
        if homework_lesson_id:
            self.queryset = self.queryset.filter(homework_lesson__id=homework_lesson_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.id
        return super(HomeworkLessonResourceViewSet, self).create(
            request, *args, **kwargs
        )
