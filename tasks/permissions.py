from rest_framework.permissions import BasePermission


class IsProjectOwner(BasePermission):
    """
    Only project owner can modify the project.
    """

    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user



class IsProjectOwnerOrMember(BasePermission):
    """
    Owner and members can view the project.
    """

    def has_object_permission(self, request, view, obj):

        if obj.owner == request.user:
            return True

        if obj.members.filter(id=request.user.id).exists():
            return True

        return False