from django.db import models
from django.utils.translation import gettext_lazy as _

from training_fyg.utils.models import BaseModel


def lesson_extra_resource_directory_path(instance, filename):
    return "courses/{0}/{1}/{2}/resources/{3}".format(
        instance.lesson.module.course.name,
        instance.lesson.module.topic,
        instance.lesson.topic,
        filename,
    )


def lesson_resource_directory_path(instance, filename):
    return "lessons-resource/{}".format(filename)


class Lesson(BaseModel):
    module = models.ForeignKey(
        to="courses.CourseModule",
        verbose_name="clase",
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    topic = models.CharField(
        max_length=100, verbose_name=_("Tema del curso"), unique=False
    )
    description = models.TextField(
        max_length=10000, verbose_name=_("Descripción del tema a tratar")
    )
    time_taken = models.PositiveIntegerField(
        verbose_name=_("Duración de la lección"),
        default=5,
        help_text=_("Tiempo tomado para completar la lección en minutos"),
    )

    class Meta:
        verbose_name = "Lección del módulo"
        verbose_name_plural = "Lecciones del módulo"

    def __str__(self):
        return self.topic


class LessonResource(BaseModel):
    resource = models.FileField(
        verbose_name="Recurso",
        upload_to="courses/image-lesson/resource/%Y/%m/%d/",
        max_length=500,
        blank=False,
        null=False,
    )
    lesson = models.ForeignKey(
        to="courses.Lesson",
        verbose_name="clase",
        on_delete=models.CASCADE,
        related_name="lessonresource",
        null=True,
    )

    class Meta:
        verbose_name = _("Recurso de la lección")
        verbose_name_plural = _("Recursos de la lección")

    def __str__(self):
        return str(self.resource)
