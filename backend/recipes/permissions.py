from . import views, models

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework import viewsets


class RecipePermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: viewsets.ModelViewSet):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(
        self,
        request: Request,
        view: viewsets.ModelViewSet,
        obj: models.Recipe
        ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ('PUT', 'DELETE'):
            return request.user == obj.author or request.user.is_staff
        return False
