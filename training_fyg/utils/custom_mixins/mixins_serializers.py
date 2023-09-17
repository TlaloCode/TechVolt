from typing import Any

from django.utils.translation import gettext_lazy as _

from rest_framework import mixins, serializers, viewsets
from rest_framework.request import Request
from rest_framework.response import Response


class ListUniqueValidator(object):
    message = _("This field must be unique.")

    def __init__(self, unique_field_names):
        self.unique_field_names = unique_field_names

    @staticmethod
    def has_duplicates(counter):
        return any([count for count in counter.values() if count > 1])

    def __call__(self, value):
        from collections import Counter

        field_counters = {
            field_name: Counter(
                item[field_name] for item in value if field_name in item
            )
            for field_name in self.unique_field_names
        }
        has_duplicates = any(
            [
                ListUniqueValidator.has_duplicates(counter)
                for counter in field_counters.values()
            ]
        )
        if has_duplicates:
            for item in value:
                error = {}
                for field_name in self.unique_field_names:
                    counter = field_counters[field_name]
                    if counter[item.get(field_name)] > 1:
                        error[field_name] = self.message
                        raise serializers.ValidationError(error)

    def __repr__(self):
        return "<%s(unique_field_names=%s)>" % (
            self.__class__.__name__,
            self.unique_field_names,
        )


class CustomCreateModelMixin(mixins.CreateModelMixin):
    """Clase para sobreescribir la creación de un objeto inyectando el usuario en el request"""

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request.data["created_by"] = request.user.id
        return super(CustomCreateModelMixin, self).create(request, *args, **kwargs)


class CustomUpdateModelMixin(mixins.UpdateModelMixin):
    """Clase para sobreescribir la actualización de un objeto inyectando el usuario en el request"""

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request.data["modified_by"] = request.user.id
        return super(CustomUpdateModelMixin, self).update(request, *args, **kwargs)


class CustomDestroyModelMixin(mixins.DestroyModelMixin):
    """Clase para sobreescribir la eliminación de un objeto cambiando el atributo is_active=False"""

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class CustomModelViewSet(
    CustomCreateModelMixin,
    CustomUpdateModelMixin,
    mixins.RetrieveModelMixin,
    CustomDestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Un ViewSet customizado para proveer el método create()"""

    pass
