from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from saturn.web.api.models import Client, Monitor, Project, Task
from saturn.web.api.serializers import ClientSerializer, MonitorSerializer, ProjectSerializer, TaskSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """client."""

    queryset = Client.objects.order_by("-id")
    serializer_class = ClientSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """project."""

    queryset = Project.objects.order_by("-id")
    serializer_class = ProjectSerializer


class MonitorViewSet(viewsets.ModelViewSet):
    """monitor."""

    queryset = Monitor.objects.order_by("-id")
    serializer_class = MonitorSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """task."""

    queryset = Task.objects.order_by("-id")
    serializer_class = TaskSerializer


@api_view(["GET"])
def status(request: Request) -> Response:
    """Status."""
    return Response({"success": 1, "error": 0, "project": 1, "request": request.path})


@api_view(["GET"])
def client_status(request: Request, client_id: int) -> Response:
    """Client status."""
    client = Client.objects.get(id=client_id)
    return Response({"result": "1" if client else "-1", "request": request.path})
