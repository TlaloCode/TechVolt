from django.core.validators import MaxValueValidator
from django.db import models

from training_fyg.utils.models import BaseModel


class CourseLessonProgress(BaseModel):
    """
    Modelo para almacenar el progreso de un usuario en las lecciones de un curso
    """

    user = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, verbose_name="Usuario"
    )
    lesson = models.ForeignKey(
        verbose_name="Lección",
        to="courses.Lesson",
        on_delete=models.CASCADE,
        help_text="Lección en proceso",
    )
    progress = models.PositiveIntegerField(
        verbose_name="Progreso de la lección",
        validators=[
            MaxValueValidator(100),
        ],
    )

    class Meta:
        verbose_name = "Progreso de la lección "
        verbose_name_plural = "Progresos de las lecciones"
        unique_together = (
            "user",
            "lesson",
        )

    def __str__(self):
        return f"{self.user} - {self.lesson} - {self.progress} %"
