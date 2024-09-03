from rest_framework import permissions


class IsVerify(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_verify:
            return True
        return False
