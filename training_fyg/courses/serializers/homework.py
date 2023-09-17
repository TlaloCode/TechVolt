import logging

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from training_fyg.courses.models import (
    HomeworkLesson,
    HomeworkLessonDelivery,
    HomeworkLessonResource,
    HomeworkLessonReview,
    Lesson,
)
from training_fyg.users.serializers.users import UserModelSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class HomeworkLessonResourceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkLessonResource
        fields = "__all__"
        extra_kwargs = {
            "is_active": {"default": True},
        }


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id",
            "topic",
            "description",
            "module",
        )


class HomeworkLessonModelSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    resources = HomeworkLessonResourceModelSerializer(
        many=True, read_only=True, source="homeworklessonresource"
    )

    # Método para guardar / actualizar sin necesidad de recibir el objeto HomeworkLesson completo
    def to_internal_value(self, data):
        self.fields["lesson"] = serializers.PrimaryKeyRelatedField(
            queryset=Lesson.objects.all()
        )
        self.fields["resources"] = serializers.PrimaryKeyRelatedField(
            queryset=HomeworkLessonResource.objects.all(),
            many=True,
            source="homeworklessonresource",
        )
        return super(HomeworkLessonModelSerializer, self).to_internal_value(data)

    class Meta:
        model = HomeworkLesson
        fields = "__all__"
        extra_kwargs = {
            "title": {"required": True},
        }

    def validate(self, attrs):
        # 1. Si al editar una tarea, ya existe otra con el mismo nombre
        #    dentro de la misma lección, se lanzará una exception.
        #    En la validación hay que buscar todas las tareas de la misma lección, excluyendo
        #    la tarea que se está editando.
        # 2. Si al añadir un módulo, ya existe otro con el mismo nombre
        #    dentro del mismo curso entonces lanzará una exception.
        if self.instance:
            # Evita que se actualice la lección de una tarea
            if attrs["lesson"].id != self.instance.lesson.id:
                raise serializers.ValidationError(
                    {"lesson": _("La lección no se puede actualizar")}
                )
            # Inicia validación de títulos iguales
            if (
                HomeworkLesson.objects.filter(
                    title=attrs["title"], lesson=attrs["lesson"], is_active=True
                )
                .exclude(id=self.instance.id)
                .count()
                > 0
            ):
                raise serializers.ValidationError(
                    {
                        "title": _(
                            "Problema al editar. Ya existe una tarea con el mismo título"
                        )
                    }
                )

        else:
            # Revisar que la tarea sea creado por el propietario de la lección
            if attrs["lesson"].created_by != attrs["created_by"]:
                raise serializers.ValidationError(
                    {
                        "created_by": _(
                            "El usuario de la tarea no corresponde con el de la lección"
                        )
                    }
                )
            if (
                HomeworkLesson.objects.filter(
                    title=attrs["title"], lesson=attrs["lesson"], is_active=True
                ).count()
                > 0
            ):
                raise serializers.ValidationError(
                    {
                        "lesson": _(
                            "Problema al crear. Ya existe una tarea con el mismo título"
                        )
                    }
                )

        return attrs


class HomeworkLessonReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkLessonReview
        fields = "__all__"
        extra_kwargs = {
            "homework_lesson_delivery": {"required": True},
            "qualification": {"required": True},
        }

    # noinspection PyMethodMayBeStatic
    def validate(self, attrs):
        if not self.instance:
            if (
                HomeworkLessonReview.objects.filter(
                    homework_lesson_delivery=attrs["homework_lesson_delivery"]
                ).count()
                > 0
            ):
                raise serializers.ValidationError(
                    {
                        "homework_lesson_delivery": _(
                            "Ya existe una revisión para esta tarea"
                        )
                    }
                )

        return attrs


class HomeworkLessonDeliverySerializer(serializers.ModelSerializer):
    homework_lesson_review = HomeworkLessonReviewSerializer(
        read_only=True, source="homeworklessonreview"
    )
    lesson_topic = serializers.SerializerMethodField(
        source="get_lesson_topic", read_only=True
    )
    module_topic = serializers.SerializerMethodField(
        source="get_module_topic", read_only=True
    )
    course_name = serializers.SerializerMethodField(
        source="get_course_name", read_only=True
    )

    # Método para guardar / actualizar sin necesidad de recibir el objeto HomeworkLesson completo
    def to_internal_value(self, data):
        self.fields["homework_lesson"] = serializers.PrimaryKeyRelatedField(
            queryset=HomeworkLesson.objects.all()
        )
        self.fields["created_by"] = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all()
        )
        return super(HomeworkLessonDeliverySerializer, self).to_internal_value(data)

    # Permite retornar el objeto serializado HomeworkLesson cuando se crea / actualiza el objeto HomeworkLessonDelivery
    def to_representation(self, obj):
        self.fields["homework_lesson"] = HomeworkLessonModelSerializer()
        self.fields["created_by"] = UserModelSerializer()
        return super(HomeworkLessonDeliverySerializer, self).to_representation(obj)

    # noinspection PyMethodMayBeStatic
    def get_lesson_topic(self, obj: HomeworkLessonDelivery):
        lesson = obj.homework_lesson.lesson
        return lesson.topic

    # noinspection PyMethodMayBeStatic
    def get_module_topic(self, obj: HomeworkLessonDelivery):
        module = obj.homework_lesson.lesson.module
        return module.topic

    # noinspection PyMethodMayBeStatic
    def get_course_name(self, obj: HomeworkLessonDelivery):
        course = obj.homework_lesson.lesson.module.course
        return course.name

    class Meta:
        model = HomeworkLessonDelivery
        fields = "__all__"
        extra_kwargs = {
            "resource": {"required": True},
            "status_type": {"read_only": True},
        }

    # noinspection PyMethodMayBeStatic
    def validate(self, attrs):
        if (
            HomeworkLessonDelivery.objects.filter(
                created_by=attrs["created_by"], homework_lesson=attrs["homework_lesson"]
            ).count()
            > 0
        ):
            raise serializers.ValidationError(
                {"homework_lesson": _("Ya existe una entrega para esta tarea")}
            )
        return attrs

    def create(self, validated_data):
        validated_data["is_active"] = True
        return super(HomeworkLessonDeliverySerializer, self).create(validated_data)
