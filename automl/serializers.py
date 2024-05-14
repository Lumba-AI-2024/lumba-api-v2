from rest_framework import serializers

from ml_model.models import AutoMLModel
from ml_model.serializers import AutoMLModelSerializer


class AutoMLSerializer(serializers.ModelSerializer):
    models = AutoMLModelSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = AutoMLModel
        fields = ('dataset', 'created_time', 'updated_time')

