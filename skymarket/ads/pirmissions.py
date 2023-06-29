
from rest_framework.permissions import BasePermission

ROLE = ["admin"]


class AuthorOrAdminPermission(BasePermission):

    message = "Не достаточно прав доступа"

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user or request.user.role in ROLE:
            return True
        return False



