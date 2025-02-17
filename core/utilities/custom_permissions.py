from rest_framework import permissions


class IsTaskOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners or admins to edit/delete a task.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.assigned_to and obj.assigned_to == request.user) or request.user.is_admin




class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners or admins to edit/delete a task.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user and obj.user == request.user

