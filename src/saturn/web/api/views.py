from rest_framework import viewsets

from saturn.web.api.models import Client
from saturn.web.api.serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """client."""

    queryset = Client.objects.order_by("-id")
    serializer_class = ClientSerializer
