"""Admin registrations for tracker models."""

from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin interface for task management."""

    list_display = ("id", "title", "owner", "priority", "status", "due_date")
    list_filter = ("priority", "status")
    search_fields = ("title", "description", "owner__username")
