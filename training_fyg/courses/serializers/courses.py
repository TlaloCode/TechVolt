import logging

from django.conf import settings
from django.utils.translation import gettext_lazy as _

import jwt
from rest_framework import serializers

from training_fyg.courses.models import (
    Course,
    CourseImage,
    CourseInvitation,
    CourseModule,
    CourseScheduleClass,
    ImagesLesson,
    Lesson,
    StudentCourse,
    TeacherCourse,
)
from training_fyg.users.models.users import User
from training_fyg.users.serializers.users import UserModelSerializer
from training_fyg.utils.custom_mixins.mixins_serializers import ListUniqueValidator

logger = logging.getLogger(__name__)


class CourseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseImage
        fields = "__all__"
        extra_kwargs = {
            "is_active": {"default": True},
        }


class UniquenessCourseModuleListSerializer(serializers.ListSerializer):
    validators = [ListUniqueValidator(unique_field_names=["topic"])]


class ModuleFromExistingCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModule
        fields = "__all__"
        extra_kwargs = {
            "course": {"write_only": True, "required": False},
        }


class CourseModuleSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        # 1. Al editar un módulo ya existe otro con el mismo nombre
        #    dentro del mismo curso entonces lanzará una exception.
        #    En la validación hay que buscar en los módulos excluyendo
        #    el módulo que se está editando.
        # 2. Si al añadir un módulo, ya existe otro con el mismo nombre
        #    dentro del mismo curso entonces lanzará una exception.
        if self.instance:
            # Evita que se actualice el curso de un módulo
            if attrs["course"].id != self.instance.course.id:
                raise serializers.ValidationError(
                    {"course": _("El curso no se puede actualizar")}
                )
            # Inicia validación de nombres iguales
            if (
                CourseModule.objects.filter(
                    course_id=attrs["course"].id, topic=attrs["topic"]
                )
                .exclude(id=self.instance.id)
                .count()
                > 0
            ):
                raise serializers.ValidationError(
                    {
                        "topic": _(
                            "Problema al editar. Ya existe un módulo con el mismo nombre"
                        )
                    }
                )

        else:
            # Revisar que el módulo sea creado por el propietario del curso
            if attrs["course"].created_by != attrs["created_by"]:
                raise serializers.ValidationError(
                    {
                        "created_by": _(
                            "El usuario del módulo no corresponde con el del curso"
                        )
                    }
                )
            if (
                CourseModule.objects.filter(
                    topic=attrs["topic"], course_id=attrs["course"].id
                ).count()
                > 0
            ):
                raise serializers.ValidationError(
                    {
                        "topic": _(
                            "Problema al crear. Ya existe un módulo con el mismo nombre"
                        )
                    }
                )

        return attrs

    class Meta:
        list_serializer_class = UniquenessCourseModuleListSerializer
        model = CourseModule
        fields = "__all__"


class CourseEditSerializer(serializers.ModelSerializer):
    course_image = CourseImageSerializer(read_only=True, source="image")

    class Meta:
        model = Course
        fields = "__all__"
        extra_kwargs = {
            "image": {"write_only": True},
        }

    def update(self, instance, validated_data):
        categories_data = validated_data.pop("categories")
        instance = super(CourseEditSerializer, self).update(instance, validated_data)

        # Comentarios de prueba
        for category in instance.categories.all():
            instance.categories.remove(category)

        for category in categories_data:
            instance.categories.add(category)
        return instance


class CourseSerializer(serializers.ModelSerializer):
    course_image = CourseImageSerializer(read_only=True, source="image")
    modules = ModuleFromExistingCourseSerializer(many=True, write_only=True)
    created_by_obj = UserModelSerializer(read_only=True, source="created_by")

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        del validated_data["modules"]
        course = super(CourseSerializer, self).create(validated_data)
        TeacherCourse.objects.create(user=user, course=course)
        return course

    class Meta:
        model = Course
        fields = "__all__"
        extra_kwargs = {
            "image": {"write_only": True},
        }


class ModelLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "is_active", "topic", "description", "time_taken")


class CourseModuleWithLessonsSerializer(serializers.ModelSerializer):
    lessons = ModelLessonSerializer(many=True)

    class Meta:
        model = CourseModule
        fields = ("id", "is_active", "topic", "description", "lessons")


class CourseLessonsSerializer(serializers.ModelSerializer):
    modules = CourseModuleWithLessonsSerializer(many=True)

    class Meta:
        model = Course
        fields = "__all__"


class CourseInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseInvitation
        fields = "__all__"


class StudentCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    def to_internal_value(self, data):
        self.fields["course"] = serializers.PrimaryKeyRelatedField(
            queryset=Course.objects.all(),
        )
        return super(StudentCourseSerializer, self).to_internal_value(data)

    # noinspection PyMethodMayBeStatic
    def validate(self, attrs):
        course = attrs["course"]
        user = attrs["user"]

        if course.course_type == Course.CourseType.PRIVATE:
            raise serializers.ValidationError(
                {
                    "course": _(
                        "Se necesita una invitación para inscribirse a un curso privado"
                    )
                }
            )
        if (
            StudentCourse.objects.filter(user_id=user.id, course_id=course.id).count()
            > 0
        ):
            raise serializers.ValidationError(
                {"course": _("El usuario ya está inscrito a este curso")}
            )
        return attrs

    class Meta:
        model = StudentCourse
        fields = "__all__"
        extra_kwargs = {
            "user": {"required": True},
        }


class ResourceEmbebedLessonSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        validated_data["is_active"] = True
        instance.is_active = True
        return super(ResourceEmbebedLessonSerializer, self).update(
            instance, validated_data
        )

    def create(self, validated_data):
        validated_data["is_active"] = True
        return super(ResourceEmbebedLessonSerializer, self).create(validated_data)

    class Meta:
        model = ImagesLesson
        fields = "__all__"


class CourseInvitationValidateSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Link de verificación ha expirado")
        except jwt.exceptions.PyJWTError:
            raise serializers.ValidationError("Token inválido")

        if payload["token_type"] != "course_confirmation":
            raise serializers.ValidationError({"token_type": "Token inválido"})

        self.context["payload"] = payload

        return data

    def create(self, **kwargs):
        payload = self.context["payload"]

        id_user = User.objects.get(email=payload["email"]).id

        logger.info("id_user" + id_user)

        if not StudentCourse.objects.filter(
            course_id=payload["id_course"], user_id=id_user
        ).exists():
            student = StudentCourse.objects.create(
                user_id=id_user, course_id=payload["id_course"]
            )
            logger.info(student)

            student.save()

            logger.info(payload["email"])
            logger.info(payload["id_course"])

            invitationcourse = CourseInvitation.objects.get(id=payload["id_invitation"])
            invitationcourse.status_invitarion = "active"
            invitationcourse.save()


class CourseScheduleClassSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(required=False, allow_null=True)

    end_date = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = CourseScheduleClass
        fields = "__all__"

    def create(self, validated_data):
        course_schedule_class = CourseScheduleClass.objects.create(**validated_data)

        if "start_date" in validated_data and validated_data["start_date"] is not None:
            course_schedule_class.start_date = validated_data["start_date"]
            course_schedule_class.save()

        return course_schedule_class


class CourseScheduleClSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseScheduleClass
        fields = [
            "course",
            "module",
            "lesson",
            "description",
            "start_date",
            "end_date",
            "url",
            "created_by",
        ]
