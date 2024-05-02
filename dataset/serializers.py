from rest_framework import serializers

from dataset.models import Dataset
from workspace.models import Workspace


class DatasetSerializer(serializers.ModelSerializer):

    workspace = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Workspace.objects.all()
    )

    class Meta:
        model = Dataset
        fields = ('file', 'name', 'username', 'numeric', 'non_numeric', 'workspace', 'size', 'created_time', 'updated_time')
