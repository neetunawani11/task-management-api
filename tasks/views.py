from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.db.models import Q

from .models import Project, Task
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
            project__owner=self.request.user
        ).filter(
            project__members=self.request.user
        ).distinct()



    def perform_create(self, serializer):

        project = serializer.validated_data["project"]


        if project.owner != self.request.user:

            if not project.members.filter(
                id=self.request.user.id
            ).exists():

                raise PermissionDenied(
                    "You cannot create tasks for this project."
                )


        serializer.save()