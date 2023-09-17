"""Users permissions classes."""
from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission

from training_fyg.users.models import UserProfileRole

User = get_user_model()


class IsAdminPermission(BasePermission):
    """Allow access only to admins."""

    def __init__(self):
        super(IsAdminPermission, self).__init__()
        self.is_admin_role = UserProfileRole.objects.get(value="ADMIN")

    def has_permission(self, request, view):
        return request.user.role == self.is_admin_role
