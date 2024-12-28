from django.http import HttpRequest, HttpResponse, JsonResponse


def index(request: HttpRequest) -> HttpResponse:
    """Index."""
    return JsonResponse({"headers": dict(request.headers.items())})
