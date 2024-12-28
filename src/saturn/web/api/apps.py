from django.apps import AppConfig


class ApiConfig(AppConfig):
    """api app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "saturn.web.api"
