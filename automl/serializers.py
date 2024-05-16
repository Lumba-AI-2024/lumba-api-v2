from rest_framework import serializers

from automl.models import AutoML
from ml_model.serializers import AutoMLModelSerializer


class AutoMLSerializer(serializers.ModelSerializer):
    models = AutoMLModelSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = AutoML
        fields = ('name', 'dataset', 'method', 'feature', 'target', 'created_time', 'updated_time', 'models')

