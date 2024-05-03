from rest_framework import serializers

from ml_model.models import MLModel
from workspace.models import Workspace

class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = ('name', 'model_file', 'dataset', 'method', 'algorithm', 'metrics', 'score',
                  'feature', 'target', 'status', 'created_time', 'updated_time')
