from django.db.models import Q

from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Project, Task
from .permissions import (
    IsProjectOwner,
    IsProjectOwnerOrMember,
    IsTaskOwnerOrAssignedUser,
)
from .serializers import (
    ProjectSerializer,
    TaskSerializer,
    RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    permission_classes = [
        AllowAny
    ]


class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()

    serializer_class = ProjectSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Project.objects.filter(
            Q(owner=self.request.user) |
            Q(members=self.request.user)
        ).distinct()

    def get_permissions(self):

        if self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [
                IsAuthenticated,
                IsProjectOwner,
            ]

        else:
            permission_classes = [
                IsAuthenticated,
                IsProjectOwnerOrMember,
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def perform_create(self, serializer):

        serializer.save(
            owner=self.request.user
        )


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()

    serializer_class = TaskSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Task.objects.filter(
            Q(project__owner=self.request.user) |
            Q(project__members=self.request.user)
        ).distinct()

    def get_permissions(self):

        if self.action == "destroy":

            permission_classes = [
                IsAuthenticated,
                IsProjectOwner,
            ]

        elif self.action in [
            "retrieve",
            "update",
            "partial_update",
        ]:

            permission_classes = [
                IsAuthenticated,
                IsTaskOwnerOrAssignedUser,
            ]

        else:

            permission_classes = [
                IsAuthenticated
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def perform_create(self, serializer):

        project = serializer.validated_data["project"]

        if project.owner != self.request.user:

            if not project.members.filter(
                id=self.request.user.id
            ).exists():

                raise PermissionDenied(
                    "You cannot create tasks for this project."
                )

        assigned_user = serializer.validated_data.get(
            "assigned_to"
        )

        if assigned_user is not None:

            if not project.members.filter(
                id=assigned_user.id
            ).exists():

                if assigned_user != project.owner:

                    raise PermissionDenied(
                        "You can only assign tasks to project members."
                    )

        serializer.save()

    def perform_update(self, serializer):

        task = self.get_object()

        is_project_owner = (
            task.project.owner == self.request.user
        )

        if not is_project_owner:

            if "assigned_to" in serializer.validated_data:

                new_assigned_user = serializer.validated_data[
                    "assigned_to"
                ]

                if new_assigned_user != task.assigned_to:

                    raise PermissionDenied(
                        "Only the project owner can assign or reassign tasks."
                    )

            if "project" in serializer.validated_data:

                new_project = serializer.validated_data[
                    "project"
                ]

                if new_project != task.project:

                    raise PermissionDenied(
                        "Only the project owner can move a task to another project."
                    )

        serializer.save()