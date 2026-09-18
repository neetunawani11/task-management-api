from rest_framework.permissions import BasePermission


class IsProjectOwner(BasePermission):
    """
    Only the project owner can modify the project.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsProjectOwnerOrMember(BasePermission):
    """
    Project owner and project members can access the project.
    """

    def has_object_permission(self, request, view, obj):

        if obj.owner == request.user:
            return True

        if obj.members.filter(id=request.user.id).exists():
            return True

        return False


class IsTaskOwnerOrAssignedUser(BasePermission):
    """
    Project owner has full access to the task.

    The user assigned to the task can view and update
    the task, but cannot delete it.
    """

    def has_object_permission(self, request, view, obj):

        user = request.user

        # Project owner has full access.
        if obj.project.owner == user:
            return True

        # Assigned user can view/update,
        # but cannot delete.
        if obj.assigned_to == user:

            if request.method == "DELETE":
                return False

            return True

        return False