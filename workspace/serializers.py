from rest_framework import serializers

from workspace.models import Workspace
from dataset.serializers import DatasetSerializer


class WorkspaceSerializer(serializers.ModelSerializer):
    datasets = DatasetSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Workspace
        fields = ('name', 'username', 'description', 'type', 'created_time', 'updated_time', 'datasets')