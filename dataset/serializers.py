from rest_framework import serializers

from dataset.models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = (
            'file', 'name', 'username', 'numeric', 'non_numeric', 'workspace', 'size', 'created_time', 'updated_time','row')