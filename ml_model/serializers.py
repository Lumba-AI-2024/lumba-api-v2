from rest_framework import serializers

from ml_model.models import MLModel, AutoMLModel


class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = ('name', 'model_file', 'dataset', 'method', 'algorithm', 'metrics', 'score',
                  'feature', 'target', 'status', 'shap_values', 'created_time', 'updated_time')


class AutoMLModelSerializer(MLModelSerializer):
    class Meta(MLModelSerializer.Meta):
        model = AutoMLModel
        fields = MLModelSerializer.Meta.fields + ('autoML_project',)
