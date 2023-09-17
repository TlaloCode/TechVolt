from django.urls import include, path

from rest_framework.routers import DefaultRouter

from training_fyg.categories.views.categories import CategoriesViewSet

router = DefaultRouter()
router.register(r"categories", CategoriesViewSet, basename="categories")

urlpatterns = [
    path("", include((router.urls, "categories"), namespace="categories")),
]
