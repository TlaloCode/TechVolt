from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter, SimpleRouter

from training_fyg.users.views.auth import UserAuthNonAtomicViewSet, UserAuthViewSet
from training_fyg.users.views.profile import ProfileViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# Auth
router.register("auth", UserAuthViewSet, basename="auth")
router.register("auth", UserAuthNonAtomicViewSet, basename="auth_not_atomic")
router.register("profile", ProfileViewSet, basename="profile")
urlpatterns = [
    path("", include((router.urls, "auth"), namespace="auth")),
]
