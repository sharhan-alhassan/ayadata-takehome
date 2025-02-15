from django.urls import path

from tasks.comments.comment import CreateCommentView, UpdateCommentView
from .task.task import AssignTaskView, TaskListCreateView, TaskDetailView
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter


app_name = "tasks"
router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("list/create/", TaskListCreateView.as_view(), name="task-list-create"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path(
        "<int:pk>/assign/<uuid:user_id>/", AssignTaskView.as_view(), name="assign-task"
    ),
    path("<int:task_id>/comments/", CreateCommentView.as_view(), name="create-comment"),
    path("comments/<int:pk>/", UpdateCommentView.as_view(), name="update-comment"),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=settings.DEBUG
)
urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=settings.DEBUG
)
