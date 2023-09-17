import json

from django.db import transaction
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions, mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from url_filter.integrations.drf import DjangoFilterBackend

from training_fyg.courses.models import (
    CourseModule,
    Lesson,
    StudentCourse,
    TeacherCourse,
)
from training_fyg.courses.permissions import IsCourseOwner
from training_fyg.courses.serializers import (
    CourseEditSerializer,
    CourseImageSerializer,
    CourseInvitationSerializer,
    CourseInvitationValidateSerializer,
    CourseLessonsSerializer,
    CourseModuleSerializer,
    CourseScheduleClassSerializer,
    CourseScheduleClSerializer,
    CourseSerializer,
    LessonSerializer,
    ResourceEmbebedLessonSerializer,
    StudentCourseSerializer,
)
from training_fyg.users.permissions.users import IsAdminPermission
from training_fyg.utils.custom_mixins.mixins_serializers import CustomModelViewSet


class CourseViewSet(CustomModelViewSet):
    serializer_class = CourseSerializer
    queryset = (
        serializer_class.Meta.model.objects.select_related("created_by")
        .select_related("image")
        .prefetch_related("modules")
        .prefetch_related("modules__lessons")
        .prefetch_related("categories")
        .filter(is_active=True)
        .order_by("id")
    )
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = [
        "created_by",
    ]

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ["destroy"]:
            permissions = [IsAuthenticated, IsAdminPermission]
        elif self.action in ["invitation"]:
            permissions = [IsAuthenticated]
        elif self.action in ["update"]:
            permissions = [IsCourseOwner]
        else:
            permissions = [IsAuthenticated]

        return (permission() for permission in permissions)

    def get_serializer_class(self):
        if self.action == "partial_update":
            raise exceptions.MethodNotAllowed(self.request.method)
        elif self.action == "update":
            self.serializer_class = CourseEditSerializer

        return self.serializer_class

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.id
        course_serializer = self.get_serializer(data=request.data)
        course_serializer.is_valid(raise_exception=True)
        course = course_serializer.save()
        # Si el curso se guarda exitosamente, ahora genera los módulos
        modules = course_serializer.validated_data["modules"]
        modules_list_dict = json.loads(json.dumps(modules))
        for module in modules_list_dict:
            module["course"] = course.id
        module_serializer = CourseModuleSerializer(data=modules_list_dict, many=True)
        module_serializer.is_valid(raise_exception=True)
        self.perform_create(module_serializer)
        headers = self.get_success_headers(course_serializer.data)
        return Response(
            course_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_destroy(self, instance):
        # Valida que el curso no tenga modulos
        if (
            CourseModule.objects.filter(
                is_active=True, course_id__in=[instance.id]
            ).count()
            > 0
        ):
            raise serializers.ValidationError(
                {"course": _("No se pueden eliminar curso con modulos activos")}
            )

        instance.is_active = False
        instance.save()

    @staticmethod
    def validate_access(self, course):
        if self.request.user.is_superuser:
            return "superuser"

        is_student = course.students.filter(user=self.request.user).exists()
        is_teacher = course.maestros.filter(user=self.request.user).exists()
        is_user_in_course = is_student or is_teacher

        if course.course_type == "private" and not is_user_in_course:
            raise exceptions.PermissionDenied(
                detail="Debe tener acceso a este curso privado"
            )

        return "student" if is_student else "teacher"

    @action(detail=False, methods=["post"])
    def invitation(self, request, *args, **kwargs):
        """invitacion course verification API view."""
        serializer = CourseInvitationValidateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"message": "Felicidades, ahora puedes ingresar a la clase"}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="get-temario")
    def get_temario(self, request, *args, **kwargs):
        if self.request.query_params.get("idCurso"):
            temario = CourseModuleSerializer.Meta.model.objects.filter(
                course_id=self.request.query_params.get("idCurso")
            )

            data = CourseModuleSerializer(temario, many=True)

        return Response(data.data)

    @action(detail=False, methods=["GET"], url_path="get-leccion")
    def get_leccion(self, request, *args, **kwargs):
        if self.request.query_params.get("idCurso") and self.request.query_params.get(
            "idModulo"
        ):
            modulos = LessonSerializer.Meta.model.objects.filter(
                module__course_id=self.request.query_params.get("idCurso"),
                module_id=self.request.query_params.get("idModulo"),
            )

            data = LessonSerializer(modulos, many=True)

        return Response(data.data)

    @action(detail=True, methods=["GET"], url_path="course-lessons")
    def course_lessons(self, request, *args, **kwargs):
        """
        Método para regresar una lista de todos los cursos, con módulos y lecciones
        """
        instance = self.get_object()
        serializer = CourseLessonsSerializer(instance)
        return Response(serializer.data)


class CourseImageViewSet(CustomModelViewSet):
    serializer_class = CourseImageSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_active=True)

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return (permission() for permission in permissions)


class CourseModuleViewSet(CustomModelViewSet):
    serializer_class = CourseModuleSerializer
    queryset = (
        serializer_class.Meta.model.objects.select_related("course")
        .filter(is_active=True)
        .order_by("id")
    )
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = [
        "course",
    ]

    def get_serializer_class(self):
        if self.action == "partial_update":
            raise exceptions.MethodNotAllowed(self.request.method)
        return super(CourseModuleViewSet, self).get_serializer_class()

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ["destroy"]:
            permissions = [IsAuthenticated, IsAdminPermission]
        else:
            permissions = [IsAuthenticated]
        return (permission() for permission in permissions)

    def perform_destroy(self, instance):
        # Valida que el módulo no tenga lecciones
        if (
            Lesson.objects.filter(is_active=True, module_id__in=[instance.id]).count()
            > 0
        ):
            raise serializers.ValidationError(
                {"course": _("No se pueden eliminar el modulo con lecciones activas")}
            )

        instance.is_active = False
        instance.save()


class StudentCourseViewSet(CustomModelViewSet):
    """Model serializer encargado de suscribir usuarios a un curso"""

    serializer_class = StudentCourseSerializer
    queryset = (
        serializer_class.Meta.model.objects.select_related("user")
        .select_related("course")
        .filter(is_active=True)
        .order_by("id")
    )
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = [
        "user",
        "course",
    ]

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [
            IsAuthenticated,
        ]
        return (permission() for permission in permissions)


class EmbebedResourcesViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    serializer_class = ResourceEmbebedLessonSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_active=True).order_by("id")
    permission_classes = []

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ["retrieve"]:
            permissions = []
        return (permission() for permission in permissions)

    def create(self, request, *args, **kwargs):
        request.data.update({"resource": request.data["upload"]})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        url = (
            "http://"
            + request.META["HTTP_HOST"]
            + request.META["PATH_INFO"]
            + str(obj.id)
            + "/"
        )
        data = dict(serializer.data)
        data.update({"url": url})

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        return HttpResponse(obj.resource.read(), content_type="image/png")


class CourseScheduleClassViewSet(CustomModelViewSet):
    serializer_class = CourseScheduleClSerializer
    queryset = (
        serializer_class.Meta.model.objects.select_related("course")
        .select_related("module")
        .select_related("lesson")
        .filter(is_active=True)
        .order_by("id")
    )

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [
            IsAuthenticated,
        ]

        return (permission() for permission in permissions)

    @action(detail=False, methods=["GET"], url_path="get-schedule-general")
    def get_schedule_general(self, request, *args, **kwargs):
        """Retorna la lista de cursos en los que el usaurio está asignado como profesor y como alumno"""
        teacher_course_qs = (
            TeacherCourse.objects.all()
            .select_related("user")
            .select_related("course")
            .filter(user__id=self.request.user.id)
            .values_list("course__id")
        )
        queryset = self.get_queryset().filter(course__in=teacher_course_qs)
        data = CourseScheduleClassSerializer(queryset, many=True)
        data = data.data

        student_course_qs = (
            StudentCourse.objects.all()
            .select_related("user")
            .select_related("course")
            .filter(user__id=self.request.user.id)
            .values_list("course__id")
        )
        queryset4 = self.get_queryset().filter(course__in=student_course_qs)
        data1 = CourseScheduleClassSerializer(queryset4, many=True)
        data1 = data1.data

        return Response({"teacher": data, "student": data1}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="get-schedule")
    def get_schedule(self, request, *args, **kwargs):
        if self.request.query_params.get("idScheduleCourse"):
            schedule = CourseScheduleClassSerializer.Meta.model.objects.filter(
                id=self.request.query_params.get("idScheduleCourse"),
            )

            data = CourseScheduleClassSerializer(schedule, many=True)

        return Response(data.data)


class CourseScheduleClViewSet(viewsets.ModelViewSet):
    serializer_class = CourseScheduleClSerializer
    queryset = (
        serializer_class.Meta.model.objects.select_related("course")
        .select_related("module")
        .select_related("lesson")
        .all()
    )

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]

        return (permission() for permission in permissions)

    def get_queryset(self):
        if self.request.user.id:
            queryset1 = super().get_queryset()
            queryset2 = (
                StudentCourse.objects.all()
                .select_related("user")
                .select_related("course")
                .filter(user__id=self.request.user.id)
                .values_list("course__id")
            )
            queryset = queryset1.filter(course__in=queryset2)

        return queryset

    @action(detail=False, methods=["GET"], url_path="get-schedule-student-ind")
    def get_schedule_student(self, request, *args, **kwargs):
        if self.request.query_params.get("idScheduleCourse"):
            schedule = CourseScheduleClassSerializer.Meta.model.objects.filter(
                id=self.request.query_params.get("idScheduleCourse"),
            )

            data = CourseScheduleClassSerializer(schedule, many=True)

        return Response(data.data)


class StudentCourseClassViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = (
        serializer_class.Meta.model.objects.select_related("image")
        .prefetch_related("categories")
        .all()
    )

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]

        return (permission() for permission in permissions)

    @action(detail=False, methods=["GET"], url_path="get-temario")
    def get_temario(self, request, *args, **kwargs):
        if self.request.query_params.get("idCurso"):
            temario = CourseModuleSerializer.Meta.model.objects.filter(
                course_id=self.request.query_params.get("idCurso")
            )

            data = CourseModuleSerializer(temario, many=True)

        return Response(data.data)

    @action(detail=False, methods=["GET"], url_path="get-leccion")
    def get_leccion(self, request, *args, **kwargs):
        if self.request.query_params.get("idCurso") and self.request.query_params.get(
            "idModulo"
        ):
            modulos = LessonSerializer.Meta.model.objects.filter(
                module__course_id=self.request.query_params.get("idCurso"),
                module_id=self.request.query_params.get("idModulo"),
            )

            data = LessonSerializer(modulos, many=True)

        return Response(data.data)

    @action(detail=False, methods=["GET"], url_path="get-cursos-publicos")
    def get_cursos_publicos(self, request, *args, **kwargs):
        queryset = super().get_queryset().filter(course_type="public")
        data = CourseSerializer(queryset, many=True)
        return Response(data.data)

    def get_queryset(self):
        if self.request.user.id:
            queryset1 = super().get_queryset()
            queryset2 = (
                StudentCourse.objects.all()
                .select_related("user")
                .select_related("course")
                .filter(user__id=self.request.user.id)
                .values_list("course__id")
            )
            queryset = queryset1.filter(id__in=queryset2)

        return queryset


class StudentInvitationViewSet(viewsets.ModelViewSet):
    serializer_class = CourseInvitationSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_active=True)

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]

        return (permission() for permission in permissions)

    def get_queryset(self):
        if self.request.user.id:
            queryset1 = super().get_queryset()
            queryset2 = (
                StudentCourse.objects.all()
                .select_related("user")
                .select_related("course")
                .filter(user__id=self.request.user.id)
                .values_list("course__id")
            )
            queryset = queryset1.filter(id__in=queryset2)

        return queryset
