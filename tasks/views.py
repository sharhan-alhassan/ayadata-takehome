from django.http import Http404
from rest_framework import generics, permissions
from core.utilities.custom_pagination import CustomPagination
from .models import Task
from tasks.serializers.serializer import CreateUpdateTaskSerializer, TaskSerializer
from rest_framework import generics, permissions
from core.utilities.custom_permissions import IsOwnerOrAdminOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound


User = get_user_model()


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method.lower() in ["post"]:
            return CreateUpdateTaskSerializer
        return TaskSerializer

    def get_paginated_response(self, data, message, status_code):
        return self.paginator.get_paginated_response(data, message, status_code)

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = self.queryset
        status_param = self.request.query_params.get("status")
        due_date = self.request.query_params.get("due_date")
        if status_param:
            queryset = queryset.filter(status=status_param)
        if due_date:
            queryset = queryset.filter(due_date=due_date)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {
                    "message": "No tasks found",
                    "data": [],
                    "status": status.HTTP_200_OK,
                }
            )
        status_param = self.request.query_params.get("status")
        due_date_param = self.request.query_params.get("due_date")
        if status_param or due_date_param:
            if not queryset.exists():
                return Response(
                    {
                        "data": "No Task(s) found for the specified search criteria",
                        "status": status.HTTP_404_NOT_FOUND,
                    }
                )

        queryset = self.paginate_queryset(queryset)
        if queryset is None:
            raise NotFound(
                detail="Pagination parameters are missing or incorrect - Check to apply pagination_class"
            )

        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(
            data=serializer.data,
            message="Task(s) retrieved successfully",
            status_code=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Task created successfully",
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
            }
        )


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method.lower() in ["put", "patch"]:
            return CreateUpdateTaskSerializer
        return TaskSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrAdminOrReadOnly()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "message": "Task retrieved successfully",
                "data": serializer.data,
                "status": status.HTTP_200_OK,
            }
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": "Task updated successfully",
                "data": serializer.data,
                "status": status.HTTP_200_OK,
            }
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Task deleted successfully",
                "status": status.HTTP_204_NO_CONTENT,
            }
        )


class AssignTaskView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrReadOnly]

    def get_serializer(self, *args, **kwargs):
        return None

    def post(self, request, pk, *args, **kwargs):
        user_id = self.kwargs["user_id"]

        try:
            task = get_object_or_404(Task, pk=pk)
        except Http404:
            return Response(
                {
                    "message": "Task not found.",
                    "status": status.HTTP_404_NOT_FOUND,
                }
            )

        user = get_object_or_404(User, pk=user_id)

        task.assigned_to = user
        task.save()

        serializer = TaskSerializer(task)
        return Response(
            {
                "message": "Task assigned successfully",
                "data": serializer.data,
                "status": status.HTTP_200_OK,
            }
        )
