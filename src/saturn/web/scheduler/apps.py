"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    """scheduler app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "saturn.web.scheduler"
