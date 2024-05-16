from django.db import models

from workspace.models import Workspace


def _upload_location(instance, datasetname):
    return f'{instance.username}/{instance.workspace.name}/{instance.workspace.type}/{datasetname}'


# Create your models here.
class Dataset(models.Model):
    file = models.FileField(upload_to=_upload_location)
    name = models.CharField(max_length=100, blank=False, null=False, default='default.csv')
    size = models.FloatField(default=0)
    username = models.CharField(max_length=100, default='default')  # Redundant. TODO: change to SerializerMethodField
    workspace = models.ForeignKey(Workspace, related_name='datasets', on_delete=models.CASCADE)
    numeric = models.TextField(blank=True)
    non_numeric = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def get_file_size(self):
        return self.file.size

    def __unicode__(self):
        return self.name

    @property
    def full_path(self):
        return f'{self.username}/{self.workspace.name}/{self.workspace.type}/{self.name}'

    class Meta:
        unique_together = ('username', 'workspace', 'name',)
