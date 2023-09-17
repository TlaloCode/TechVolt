from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CourseConfig(AppConfig):
    name = "training_fyg.courses"
    verbose_name = _("Courses")
