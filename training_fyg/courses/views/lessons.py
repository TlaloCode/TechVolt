from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions, mixins, serializers, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from url_filter.integrations.drf import DjangoFilterBackend

from training_fyg.courses.models.courses import HomeworkLesson, HomeworkLessonDelivery
from training_fyg.courses.serializers import LessonResourceSerializer, LessonSerializer
from training_fyg.utils.custom_mixins.mixins_serializers import CustomModelViewSet


class LessonResourceViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    serializer_class = LessonResourceSerializer
    queryset = LessonResourceSerializer.Meta.model.objects.all()

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [
            IsAuthenticated,
        ]
        return (permission() for permission in permissions)


class LessonViewSet(CustomModelViewSet):
    serializer_class = LessonSerializer
    queryset = (
        LessonSerializer.Meta.model.objects.prefetch_related("lessonresource")
        .filter(is_active=True)
        .order_by("id")
    )
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = [
        "module",
    ]

    def get_serializer_class(self):
        if self.action == "partial_update":
            raise exceptions.MethodNotAllowed(self.request.method)
        return self.serializer_class

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in [
            "destroy",
        ]:
            permissions = [
                IsAuthenticated,
                IsAdminUser,
            ]
        else:
            permissions = [
                IsAuthenticated,
            ]
        return (permission() for permission in permissions)

    def perform_destroy(self, instance):
        # Valida que las lecciones no tenga notas
        if (
            HomeworkLesson.objects.filter(
                is_active=True, lesson_id__in=[instance.id]
            ).count()
            > 0
        ):
            raise serializers.ValidationError(
                {"course": _("No se pueden eliminar una lección con tareas activas")}
            )

        if (
            HomeworkLessonDelivery.objects.filter(
                is_active=True, homework_lesson_id__in=[instance.id]
            ).count()
            > 0
        ):
            raise serializers.ValidationError(
                {"course": _("No se pueden eliminar una lección con entregas activas")}
            )

        instance.is_active = False
        instance.save()
