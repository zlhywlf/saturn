from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    """scheduler app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "saturn.web.scheduler"
