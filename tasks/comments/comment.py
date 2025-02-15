from rest_framework import generics, permissions, status
from rest_framework.response import Response
from core.utilities.custom_permissions import IsCommentOwnerOrReadOnly
from tasks.models import Comment, Task
from tasks.serializers.serializer import CreateUpdateCommentSerializer


class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateUpdateCommentSerializer

    def perform_create(self, serializer):
        task_id = self.kwargs.get("task_id")
        task = generics.get_object_or_404(Task, id=task_id)
        serializer.save(user=self.request.user, task=task)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Comment created successfully",
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )


class UpdateCommentView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateUpdateCommentSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [IsCommentOwnerOrReadOnly()]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": "Comment updated successfully",
                "data": serializer.data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
