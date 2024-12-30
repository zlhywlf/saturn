from rest_framework import serializers

from saturn.web.api.models import Client


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    """client."""

    class Meta:
        """meta."""

        model = Client
        fields = "__all__"
