from rest_framework import permissions

class IsInstructor(permissions.BasePermission):
    """
    Allow access only to users with instructor role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'instructor'
