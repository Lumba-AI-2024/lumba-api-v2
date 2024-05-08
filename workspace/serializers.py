from rest_framework import serializers

from workspace.models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workspace
        fields = ('name', 'username', 'description', 'type', 'created_time', 'updated_time')