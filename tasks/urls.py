from django.urls import path
from .views import AssignTaskView, TaskListCreateView, TaskDetailView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list-create"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path(
        "<int:pk>/assign/<uuid:user_id>/", AssignTaskView.as_view(), name="assign-task"
    ),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=settings.DEBUG
)
urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=settings.DEBUG
)
