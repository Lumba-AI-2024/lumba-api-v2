from django.db import models


# Create your models here.
class Workspace(models.Model):
    """
    TODO: refactor this so that it uses Django's user instead of username
    """
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    username = models.CharField(max_length=100, default="default")
    description = models.CharField(max_length=200, default="default")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @property
    def full_path(self):
        return f"{self.username}/{self.name}"

    class Meta:
        unique_together = ('username', 'name',)
