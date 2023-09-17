from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter, SimpleRouter

from training_fyg.courses.views import (
    CourseImageViewSet,
    CourseLessonProgressViewSet,
    CourseModuleViewSet,
    CourseScheduleClassViewSet,
    CourseViewSet,
    EmbebedResourcesViewSet,
    HomeworkLessonDeliveryViewSet,
    HomeworkLessonResourceViewSet,
    HomeworkLessonReviewViewSet,
    HomeworkLessonViewSet,
    LessonResourceViewSet,
    LessonViewSet,
    StudentCourseViewSet,
    StudentInvitationViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "courses"

# Course
router.register("courses", CourseViewSet, basename="courses")
router.register(
    "courses-progress", CourseLessonProgressViewSet, basename="course-progress"
)
router.register("course-image", CourseImageViewSet, basename="course-image")
router.register("modules", CourseModuleViewSet, basename="modules")
router.register("student-course", StudentCourseViewSet, basename="student-course")
router.register(
    "embebed-resources", EmbebedResourcesViewSet, basename="embebed-resources"
)
router.register("homework-lesson", HomeworkLessonViewSet, basename="homework-lesson")
router.register(
    "homework-lesson-review",
    HomeworkLessonReviewViewSet,
    basename="homework-lesson-review",
)
router.register(
    "homework-lesson-delivery",
    HomeworkLessonDeliveryViewSet,
    basename="homework-lesson-delivery",
)
router.register(
    "homework-lesson-resource",
    HomeworkLessonResourceViewSet,
    basename="homework-lesson-resource",
)
router.register(
    "course-schedule-class",
    CourseScheduleClassViewSet,
    basename="course-schedule-class",
)
router.register(
    "invitaciones-alumno",
    StudentInvitationViewSet,
    basename="invitaciones-alumno",
)

router.register("lessons", LessonViewSet, basename="lessons")
router.register("lessons-resource", LessonResourceViewSet, basename="lessons-resource")


urlpatterns = [
    path("", include((router.urls, "courses"), namespace="courses")),
]
