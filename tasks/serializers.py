from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Project, Task


User = get_user_model()



class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
        ]


    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )

        return user





class ProjectSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(
        source="owner.username"
    )


    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )


    class Meta:

        model = Project

        fields = [
            "id",
            "name",
            "description",
            "owner",
            "members",
            "created_at",
            "updated_at",
        ]





class TaskSerializer(serializers.ModelSerializer):


    class Meta:

        model = Task

        fields = [
            "id",
            "project",
            "title",
            "description",
            "assigned_to",
            "status",
            "priority",
            "due_date",
            "created_at",
            "updated_at",
        ]