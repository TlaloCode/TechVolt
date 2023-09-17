from rest_framework import serializers

from training_fyg.categories.models.categories import CategoryCourse


class CategoryCourseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryCourse
        fields = (
            "id",
            "name",
            "is_active",
        )

    def validate(self, attrs):
        if CategoryCourse.objects.filter(is_active=True, name=attrs["name"]):
            raise serializers.ValidationError(
                {"name": "Ya existe una categoría con el mismo nombre"}
            )
        return attrs
