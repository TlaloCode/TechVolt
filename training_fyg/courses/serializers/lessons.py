from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from training_fyg.courses.models import Lesson, LessonResource


class LessonResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonResource
        fields = "__all__"
        extra_kwargs = {
            "is_active": {"default": True},
        }


class LessonSerializer(serializers.ModelSerializer):
    resources = LessonResourceSerializer(
        many=True, read_only=True, source="lessonresource"
    )

    # Método para guardar / actualizar sin necesidad de recibir el objeto HomeworkLesson completo
    def to_internal_value(self, data):
        self.fields["resources"] = serializers.PrimaryKeyRelatedField(
            queryset=LessonResource.objects.all(),
            many=True,
            source="lessonresource",
        )
        return super(LessonSerializer, self).to_internal_value(data)

    def validate(self, attrs):
        module_id = attrs["module"].id

        if self.instance:  # 'instance' will be set in case of `PUT` request i.e update
            lesson_id = self.instance.id  # get the 'id' for the instance
            if (
                Lesson.objects.filter(module_id=module_id, topic=attrs["topic"])
                .exclude(id=lesson_id)
                .exists()
            ):
                raise serializers.ValidationError(
                    {
                        "topic": "Ya existe una lección con el mismo tema en el módulo actual"
                    }
                )
        else:
            # Revisa que el creador de la lección coincida con el creado del módulo
            if attrs["module"].created_by != attrs["created_by"]:
                raise serializers.ValidationError(
                    {
                        "created_by": _(
                            "El usuario de la lección no corresponde con el del módulo"
                        )
                    }
                )
            if Lesson.objects.filter(
                module_id=module_id, topic=attrs["topic"]
            ).exists():
                raise serializers.ValidationError(
                    {
                        "topic": "Ya existe una lección con el mismo tema en el módulo actual"
                    }
                )
        return attrs

    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {
            "is_active": {"default": True},
            "time_taken": {"required": True},
        }
