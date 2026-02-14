"""Application configuration for tracker app."""

from django.apps import AppConfig


class TrackerConfig(AppConfig):
    """Configure task tracker application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "tracker"
