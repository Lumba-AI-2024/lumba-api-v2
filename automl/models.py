from django.db import models

from dataset.models import Dataset

# TODO: this should be a class (or classes) of enums
algorithms = {
    'REGRESSION' : ('LINEAR', 'DECISION_TREE', 'RANDOM_FOREST', 'NEURAL_NETWORK', 'XG_BOOST')
}

# Create your models here.
class AutoML(models.Model):
    name = models.CharField()
    dataset = models.ForeignKey(Dataset, related_name='datasets', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def initiate_project(self):
        """
        Initiate preprocessings, and then initiate training for each preprocesses
        :return:
        """
        pass
