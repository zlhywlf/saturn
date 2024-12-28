"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from django.urls import path

from saturn.web.scheduler import views

urlpatterns = [
    path("", views.index, name="index"),
]
