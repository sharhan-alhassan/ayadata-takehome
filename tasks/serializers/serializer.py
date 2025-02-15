from rest_framework import serializers
from tasks.models import Task
from django.contrib.auth import get_user_model
from tasks.models import Comment


User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "created_at"]

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = CustomUserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Task
        fields = ("id", "title", "status", "due_date", "assigned_to", "comments")


class CreateUpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ["assigned_to"]


class CreateUpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]

