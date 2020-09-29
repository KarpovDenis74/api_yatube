from rest_framework.permissions import BasePermission, SAFE_METHODS


class OnlyCreatorPermission(BasePermission):
    massage = "Нет прав на данное действие"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user == obj.author
        return True
