from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    """UserModelSerializer."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "email",
            "last_name",
            "second_last_name",
            "get_full_name",
            "role",
            "picture",
            "phone_number",
            "created_at",
        )
        read_only_fields = ("username", "role", "picture")

    def create(self, validated_date):
        return super(UserModelSerializer, self).create(validated_date)


class UserPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "picture")
