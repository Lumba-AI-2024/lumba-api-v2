from django.db import models

from workspace.models import Workspace


def _upload_location(instance, filename):
    return f'{instance.username}/{instance.workspace.name}/{filename}'

# Create your models here.
class Dataset(models.Model):
    file = models.FileField(unique=True, upload_to=_upload_location)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True, default='default.csv')
    size = models.FloatField(default=0)
    username = models.CharField(max_length=100, default='default')
    workspace = models.ForeignKey(Workspace, related_name='datasets', on_delete=models.CASCADE)
    # TODO: implement these
    numeric = models.TextField(blank=True)
    non_numeric = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def get_file_size(self):
        return self.file.size

    def __unicode__(self):
        return self.name