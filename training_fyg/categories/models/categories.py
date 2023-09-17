"""Day of the week catalog model."""

from django.db import models

from training_fyg.utils.models import BaseModel


class CategoryCourse(BaseModel):
    name = models.CharField(
        verbose_name="Nombre de la categoría", max_length=100, unique=False
    )

    class Meta:
        verbose_name = "Categoria de cursos"
        verbose_name_plural = "Categorias de cursos"

    def __str__(self):
        return self.name
