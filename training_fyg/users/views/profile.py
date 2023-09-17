"""User auth views."""

from django.contrib.auth import get_user_model

from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from training_fyg.users.serializers.users import (
    UserModelSerializer,
    UserPictureSerializer,
)

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    """User authentication API view."""

    serializer_class = UserModelSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_active=True)

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return (permission() for permission in permissions)

    def get_serializer_class(self):
        if self.action == "partial_update":
            raise exceptions.MethodNotAllowed(self.request.method)
        return self.serializer_class

    @action(
        detail=False,
        methods=["get"],
        url_name="get-me-profile",
        url_path="get-me-profile",
    )
    def get_me_profile(self, request, *args, **kwargs):
        data = self.serializer_class(request.user, context={"request": request})
        return Response(data.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_name="users",
        url_path="users",
    )
    def users(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserModelSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=[
            "PUT",
        ],
        url_name="update-picture-profile",
        url_path="update-picture-profile",
    )
    def update_picture_profile(self, request, *args, **kwargs):
        self.serializer_class = UserPictureSerializer
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
