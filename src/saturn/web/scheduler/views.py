"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from django.http import HttpRequest, HttpResponse, JsonResponse


def index(request: HttpRequest) -> HttpResponse:
    """Index."""
    return JsonResponse({"headers": dict(request.headers.items())})
