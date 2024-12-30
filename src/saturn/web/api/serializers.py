from rest_framework import serializers

from saturn.web.api.models import Client, Monitor, Project, Task


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    """client."""

    class Meta:
        """meta."""

        model = Client
        fields = "__all__"


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    """project."""

    class Meta:
        """meta."""

        model = Project
        fields = "__all__"


class MonitorSerializer(serializers.HyperlinkedModelSerializer):
    """monitor."""

    class Meta:
        """meta."""

        model = Monitor
        fields = "__all__"


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    """task."""

    class Meta:
        """meta."""

        model = Task
        fields = "__all__"
