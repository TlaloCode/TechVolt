from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from training_fyg.utils.models import BaseModel


def course_directory_path(instance, filename):
    """No se elimina la función para no romper migraciones"""
    return ""


def homework_lesson_resource_directory_path(instance, filename):
    """No se elimina la función para no romper migraciones"""
    return ""


class CourseModule(BaseModel):
    course = models.ForeignKey(
        verbose_name=_("Course"),
        to="courses.Course",
        related_name="modules",
        on_delete=models.CASCADE,
    )

    topic = models.CharField(max_length=100, verbose_name="Tema del curso")

    description = models.TextField(
        max_length=10000, verbose_name="Descripción del tema a tratar"
    )

    class Meta:
        verbose_name = "Módulo del curso"
        verbose_name_plural = "Módulos del curso"

    def __str__(self):
        return self.topic


class CourseImage(BaseModel):
    image = models.ImageField(
        verbose_name=_("Imagen"),
        upload_to="courses/courses/course-image/image/%Y/%m/%d/",
        max_length=1000,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("Imagen des curso")
        verbose_name_plural = _("Imágenes del curso")

    def __str__(self):
        return str(self.image)


class Course(BaseModel):
    class CourseType(models.TextChoices):
        PUBLIC = "public", "public"
        PRIVATE = "private", "private"

    name = models.CharField(
        max_length=100, verbose_name="Nombre del curso", unique=True
    )
    description = models.TextField(
        max_length=10000, verbose_name="Descripción del curso"
    )
    image = models.ForeignKey(
        verbose_name="Imagen del curso",
        to="courses.CourseImage",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    categories = models.ManyToManyField(
        to="categories.CategoryCourse", related_name="courses", blank=True
    )
    course_type = models.CharField(
        max_length=12,
        verbose_name="Tipo de curso",
        choices=CourseType.choices,
        help_text="Tipo de curso, accesible públicamente o por invitación",
    )

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.name


class StudentCourse(BaseModel):
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Estudiante del curso"),
    )

    course = models.ForeignKey(
        to="courses.Course",
        on_delete=models.CASCADE,
        verbose_name=_("Curso"),
        related_name="students",
    )

    class Meta:
        verbose_name = "Registro de estudiante en curso"
        verbose_name_plural = "Registros de estudiantes en cursos"
        unique_together = (
            "user",
            "course",
        )

    def __str__(self):
        return f"estudiante: {self.user}, curso: {self.course}"


class TeacherCourse(BaseModel):
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="profesor en un curso",
        help_text="registro de profesor en un curso",
    )

    course = models.ForeignKey(
        to="courses.Course",
        on_delete=models.CASCADE,
        verbose_name=_("Curso"),
        related_name="teachercourse",
    )

    class Meta:
        verbose_name = "Registro de maestro en curso"
        verbose_name_plural = "Registros de maestros en cursos"

    def __str__(self):
        return f"maestro: {self.user}, curso: {self.course}"


class CourseInvitation(BaseModel):
    course = models.ForeignKey(
        to="courses.Course", on_delete=models.CASCADE, verbose_name=_("Curso")
    )

    email = models.TextField(max_length=10000, verbose_name=_("Email"))

    class Meta:
        verbose_name = _("Invitacion al curso")
        verbose_name_plural = _("Invitaciones a los cursos")

    def __str__(self):
        return self.email


class ImagesLesson(BaseModel):
    resource = models.FileField(
        verbose_name=_("Recurso de la clase"),
        help_text=_("Son los recursos que se mostraran"),
        upload_to="courses/courses/images-lesson/resource/%Y/%m/%d/",
        max_length=1000,
    )

    class Meta:
        verbose_name = _("Recurso de la clase")
        verbose_name_plural = _("Recurso de la clase")

    def __str__(self):
        return str(self.resource)


class HomeworkLesson(BaseModel):
    lesson = models.ForeignKey(
        to="courses.Lesson",
        verbose_name=_("Tarea de la lección"),
        on_delete=models.CASCADE,
        related_name="homeworklesson",
    )

    title = models.CharField(
        verbose_name=_("Título"),
        max_length=120,
        default=_("Título de la tarea"),
        blank=False,
        null=False,
    )

    description = models.TextField(
        max_length=10000, verbose_name=_("Descripción de la tarea")
    )

    class Meta:
        verbose_name = _("Tarea de la lección")
        verbose_name_plural = _("Tareas de las lecciones")

    def __str__(self):
        return self.title


class HomeworkLessonReview(BaseModel):
    homework_lesson_delivery = models.OneToOneField(
        to="courses.HomeworkLessonDelivery",
        verbose_name=_("Revisión de la tarea de lección"),
        on_delete=models.CASCADE,
        related_name="homeworklessonreview",
        null=False,
        default=1,
    )
    qualification = models.FloatField(
        verbose_name=_("Calificación"),
        default=0,
        null=False,
        blank=False,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(00),
        ],
    )
    review = models.TextField(
        max_length=10000,
        verbose_name=_("Revision de la tarea"),
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = _("Revisión de tarea de la lección")
        verbose_name_plural = _("Revisiones de tareas de las lecciones")

    def __str__(self):
        return str(self.id)


class HomeworkLessonResource(BaseModel):
    homework_lesson = models.ForeignKey(
        to="courses.HomeworkLesson",
        verbose_name=_("Tarea de la lección"),
        on_delete=models.CASCADE,
        related_name="homeworklessonresource",
        null=True,
    )

    description = models.TextField(
        max_length=10000,
        verbose_name=_("Descripción"),
        null=True,
        blank=True,
    )

    resource = models.FileField(
        verbose_name=_("Recurso de la tarea"),
        upload_to="courses/courses/homework-lesson-resource/resource/%Y/%m/%d/",
        max_length=1000,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Recurso de la tarea")
        verbose_name_plural = _("Recursos de las tareas")

    def __str__(self):
        return str(self.resource)


class CourseScheduleClass(BaseModel):
    """
    Live classes for courses
    """

    course = models.ForeignKey(
        verbose_name=_("Curso"),
        to="courses.Course",
        on_delete=models.CASCADE,
    )

    module = models.ForeignKey(
        verbose_name=_("Módulo"),
        to="courses.CourseModule",
        on_delete=models.CASCADE,
        null=True,
    )

    lesson = models.ForeignKey(
        verbose_name=_("Lección"),
        to="courses.Lesson",
        on_delete=models.CASCADE,
        null=True,
    )

    description = models.TextField(
        verbose_name=_("Descripción"),
        max_length=10000,
        null=True,
        blank=True,
    )

    url = models.URLField(
        verbose_name=_("Url de la clase"),
        default="https://calendar.google.com",
        null=False,
        blank=False,
    )

    start_date = models.DateTimeField(
        verbose_name=_("Fecha inicio"),
    )

    end_date = models.DateTimeField(
        verbose_name=_("Fecha fin"),
    )

    class Meta:
        verbose_name = _("Clase que el profesor puede agendar en vivo")
        verbose_name_plural = _("Clases que el profesor puede agendar en vivo")

    def __str__(self):
        return self.description


class HomeworkLessonDelivery(BaseModel):
    """
    Modelo utilizado para los estudiantes para la entrega de tareas
    """

    class StatusType(models.TextChoices):
        REVISADO = "Revisado", "Revisado"
        PENDIENTE = "Pendiente", "Pendiente"

    note = models.CharField(
        verbose_name=_("Nota"),
        help_text=_("Notas de la entrega de la tarea"),
        max_length=200,
    )
    resource = models.FileField(
        verbose_name=_("Archivo adjunto"),
        help_text=_("Archivo adjunto"),
        null=True,
        blank=True,
    )
    homework_lesson = models.ForeignKey(
        to="courses.HomeworkLesson",
        verbose_name=_("Tarea de la lección"),
        on_delete=models.CASCADE,
        null=False,
    )

    status_type = models.CharField(
        max_length=10,
        verbose_name=_("Estatus revision"),
        help_text=_("Estatus revision"),
        choices=StatusType.choices,
        default=StatusType.PENDIENTE,
    )

    class Meta:
        verbose_name = _("Entrega de tareas")
        verbose_name_plural = _("Entregas de tareas")

    def __str__(self):
        return self.note
