from django.contrib import admin

from training_fyg.categories.models.categories import CategoryCourse


@admin.register(CategoryCourse)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_display_links = ("id", "name")
    search_fields = ("name",)
