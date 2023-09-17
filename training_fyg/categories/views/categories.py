from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from training_fyg.categories.models import CategoryCourse
from training_fyg.categories.serializers.categories import CategoryCourseModelSerializer
from training_fyg.courses.models import Course
from training_fyg.users.permissions.users import IsAdminPermission


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = CategoryCourse.objects.filter(is_active=True).order_by("name")
    serializer_class = CategoryCourseModelSerializer
    pagination_class = None

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in [
            "destroy",
        ]:
            permissions = [
                IsAuthenticated,
                IsAdminPermission,
            ]
        else:
            permissions = [
                IsAuthenticated,
            ]
        return (permission() for permission in permissions)

    def perform_destroy(self, instance):
        # Valida que la lección no tenga cursos

        if Course.objects.filter(categories__in=[instance.id]).count() > 0:
            raise serializers.ValidationError(
                {"categories": _("No se pueden eliminar categorías con cursos activos")}
            )

        instance.is_active = False
        instance.save()
