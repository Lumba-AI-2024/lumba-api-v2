import requests
from django.db import models

from dataset.models import Dataset
from lumba_api_v2 import settings


def _upload_location(instance, datasetname):
    return f'{instance.dataset.workspace.username}/{instance.dataset.workspace.name}/{datasetname}'


# Create your models here.
# format nama model: Algorithm + dataset
# format nama dataset: method + datasetname
# random_forest/standard_scaler/affairs
class MLModel(models.Model):
    name = models.CharField(max_length=100, default='')
    model_file = models.FileField(upload_to=_upload_location, blank=True)
    dataset = models.ForeignKey(Dataset, related_name='models', on_delete=models.CASCADE)
    method = models.CharField(max_length=100, default="-")  # TODO: change to enums
    algorithm = models.CharField(max_length=100, default="-")  # TODO: change to enums
    metrics = models.CharField(max_length=100, default="-")
    score = models.FloatField(default=0)
    feature = models.TextField(blank=True)
    target = models.TextField(blank=True)
    status = models.CharField(max_length=100, default="accepted")  # TODO: change to enums
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('dataset', 'name',)

    def initiate_training(self, scaled_X=None, y_target=None):
        if scaled_X is not None and y_target is not None:
            # Convert scaled_X and y_target to JSON format
            scaled_X_json = scaled_X.to_json(orient='split')
            y_target_json = y_target.to_json(orient='split')
            
            payload = {
                'modelname': self.name,
                'datasetname': self.dataset.name,
                'workspace': self.dataset.workspace.name,
                'type': self.dataset.workspace.type,
                'username': self.dataset.username,
                'method': self.method,
                'algorithm': self.algorithm,
                'metrics': self.metrics,
                'feature': self.feature,
                'target': self.target,
                'scaled_X': scaled_X_json,
                'y_target': y_target_json,
            }

            requests.post(settings.TRAINING_API_URL, json=payload)
        else:
            payload = {
                'modelname': self.name,
                'datasetname': self.dataset.name,
                'workspace': self.dataset.workspace.name,
                'type': self.dataset.workspace.type,
                'username': self.dataset.username,
                'dataset_link': self.dataset.file.url,
                'method': self.method,
                'algorithm': self.algorithm,
                'metrics': self.metrics,
                'feature': self.feature,
                'target': self.target,
            }

            requests.post(settings.TRAINING_API_URL, data=payload)

        return payload



class AutoMLModel(MLModel):
    autoML_project = models.ForeignKey('automl.AutoML', related_name='automlmodels', on_delete=models.CASCADE)

