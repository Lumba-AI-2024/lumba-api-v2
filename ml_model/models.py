from django.db import models

from dataset.models import Dataset


def _upload_location(instance, filename):
    return f'{instance.dataset.workspace.username}/{instance.dataset.workspace.name}/{filename}'


# Create your models here.
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

    def initiate_training(self):
        payload = {
            'modelname': self.name,
            'datasetname': self.dataset.name,
            'workspace': self.dataset.workspace.name,
            'type': self.dataset.workspace.type,
            'username': self.dataset.username,
            'dataset_link': self.dataset.full_path,
            'method': self.method,
            'algorithm': self.algorithm,
            'metrics': self.metrics,
            'feature': self.feature,
            'target': self.target,
        }

        return payload
