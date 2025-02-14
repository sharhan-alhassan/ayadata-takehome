from rest_framework import serializers
from tasks.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = CustomUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ("id", "title", "status", "due_date", "assigned_to")


class CreateUpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ["assigned_to"]
