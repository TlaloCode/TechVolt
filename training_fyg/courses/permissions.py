"""Users permissions classes."""
import logging

from rest_framework.permissions import BasePermission, exceptions

from training_fyg.courses.models import Course, CourseModule, HomeworkLesson, Lesson

LOG = logging.getLogger(__name__)


class IsCourseOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Verifica que un usuario sea maestro del curso"""
        user = request.user
        # Verifica el tipo de objeto
        # Valida la pertenencia sobre el objeto dependiendo del tipo
        type_obj = type(obj).__name__
        if type_obj == "Course":
            course: Course = obj
            if not course.teachercourse.filter(user=user).exists():
                raise exceptions.PermissionDenied(
                    detail="Para actualizar este curso, debe de ser un maestro en este curso"
                )
        elif type_obj == "CourseModule":
            module: CourseModule = obj
            if not module.course.teachercourse.filter(user=user).exists():
                raise exceptions.PermissionDenied(
                    detail="Para actualizar este módulo, debe de ser un maestro en este curso"
                )
        elif type_obj == "Lesson":
            lesson: Lesson = obj
            if not lesson.module.course.teachercourse.filter(user=user).exists():
                raise exceptions.PermissionDenied(
                    detail="Para actualizar esta lección, debe de ser un maestro en este curso"
                )

        elif type_obj == "HomeworkLesson":
            homework: HomeworkLesson = obj
            if not homework.lesson.module.course.teachercourse.filter(
                user=user
            ).exists():
                raise exceptions.PermissionDenied(
                    detail="Para actualizar esta tarea, debe de ser un maestro en este curso"
                )
        return True
