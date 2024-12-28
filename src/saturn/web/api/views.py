from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def index(request: Request) -> Response:
    """Index."""
    return Response({"headers": dict(request.headers.items()), "user": request.user.is_authenticated})
