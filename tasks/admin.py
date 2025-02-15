from django.contrib import admin
from .models import Task, Comment


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "assigned_to", "status")
    list_filter = ("title", "created_at")
    search_fields = ("assigned_to",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "user", "created_at")
    list_filter = ("user", "created_at")
    search_fields = ("task", "user")
    
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
