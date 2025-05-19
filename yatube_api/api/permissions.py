from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    "Permission разрешает только чтение объектов."

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
