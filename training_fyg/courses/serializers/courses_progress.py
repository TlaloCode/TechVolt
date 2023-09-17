from rest_framework import serializers

from training_fyg.courses.models import CourseLessonProgress


class CourseLessonProgressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLessonProgress
        fields = (
            "id",
            "lesson",
            "progress",
            "user",
        )
