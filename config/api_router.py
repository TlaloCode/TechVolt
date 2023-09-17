from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

# from training_fyg.users.views.auth import (
#     UserAuthNonAtomicViewSet,
#     UserAuthViewSet,
# )
# from training_fyg.users.views.user_addresses import UserAddressesViewSet
# from training_fyg.users.views.users import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# # Auth
# router.register("auth", UserAuthViewSet, basename="auth")
# router.register("auth", UserAuthNonAtomicViewSet, basename="auth_not_atomic")
# router.register("users", UserViewSet, basename="users")
# router.register("user-addresses", UserAddressesViewSet, basename="user-addresses")

app_name = "api"

urlpatterns = [
    path("", include("training_fyg.categories.urls")),
    path("", include("training_fyg.courses.urls")),
    path("", include("training_fyg.users.urls")),
    path(
        "token/",
        include(
            [  # noqa DJ05
                path("refresh/", TokenRefreshView.as_view(), name="token_refresh")
            ]
        ),
    ),
]
