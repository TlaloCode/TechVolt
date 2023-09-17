"""User models admin."""
from django.contrib import admin

from training_fyg.courses.models import (
    Course,
    CourseImage,
    CourseInvitation,
    CourseLessonProgress,
    CourseModule,
    CourseScheduleClass,
    HomeworkLesson,
    HomeworkLessonDelivery,
    HomeworkLessonResource,
    HomeworkLessonReview,
    Lesson,
    LessonResource,
    StudentCourse,
    TeacherCourse,
)

admin.site.register(CourseInvitation)
admin.site.register(CourseScheduleClass)
admin.site.register(HomeworkLessonReview)
admin.site.register(TeacherCourse)
admin.site.register(LessonResource)


@admin.register(HomeworkLessonDelivery)
class HomeworkLessonDeliveryModelAdmin(admin.ModelAdmin):
    list_display = ("id", "note", "resource", "status_type", "homework_lesson")
    list_display_links = ("id", "note")


@admin.register(HomeworkLessonResource)
class HomeworkLessonResourceModelAdmin(admin.ModelAdmin):
    list_display = ("id", "resource")
    list_display_links = ("id", "resource")


@admin.register(HomeworkLesson)
class HomeworkLessonModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "lesson")
    list_display_links = ("id", "title")


@admin.register(StudentCourse)
class StudentCourseModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course")
    list_display_links = (
        "id",
        "user",
        "course",
    )


@admin.register(CourseImage)
class CourseImageModelAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "is_active")
    list_display_links = (
        "id",
        "image",
    )


@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "course_type", "image", "created_by", "is_active")
    list_display_links = (
        "id",
        "name",
    )
    list_editable = (
        "course_type",
        "image",
        "created_by",
    )


@admin.register(CourseModule)
class CourseModuleModelAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "topic", "is_active")
    list_display_links = ("id",)
    list_editable = ("course", "topic")


@admin.register(Lesson)
class LessonModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "module",
        "topic",
        "is_active",
    )
    list_display_links = (
        "id",
        "module",
    )
    list_editable = ("topic",)


@admin.register(CourseLessonProgress)
class CourseLessonProgressModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "lesson",
        "lesson_id",
        "progress",
    )
    list_display_links = (
        "id",
        "user",
    )
