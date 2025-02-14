from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "assigned_to", "status")
    list_filter = ("title", "created_at")
    search_fields = ("assigned_to",)


admin.site.register(Task, TaskAdmin)
