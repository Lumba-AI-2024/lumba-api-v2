from django.db import models

from data_science.preprocess import Preprocess
from dataset.models import Dataset
from dataset.serializers import DatasetSerializer
from ml_model.serializers import MLModelSerializer, AutoMLModelSerializer

# TODO: this should be a class (or classes) of enums
algorithms = {
    'REGRESSION': ('LINEAR', 'DECISION_TREE', 'RANDOM_FOREST', 'NEURAL_NETWORK', 'XG_BOOST'),
    'CLASSIFICATION': ('DECISION_TREE', 'RANDOM_FOREST', 'NEURAL_NETWORK', 'XG_BOOST'),
    'CLUSTERING': ('KMEANS', 'DBSCAN')
}


# Create your models here.
class AutoML(models.Model):
    name = models.CharField(max_length=100)
    dataset = models.ForeignKey(Dataset, related_name='datasets', on_delete=models.CASCADE)
    method = models.CharField(max_length=100, default="-")
    feature = models.TextField(blank=True)
    target = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def initiate_project(self):
        """
        Initiate preprocessing, and then initiate training for each preprocesses
        :return:
        """
        models_generated = []

        for scaling in ('vanilla', 'normalization', 'standardization'):
            columns = f"{self.feature},{self.target}"
            columns = ','.join(columns.split())

            columns = columns.split(',')
            preprocess = Preprocess(dataset=Dataset.objects.get(pk=self.dataset.pk), columns=columns, target_columns=self.target)

            # handle null, duplicate, ordinal encoding, encoding, and scaling
            preproc_kwargs = {
                'missing': '1',
                'columns_missing': '',
                'duplication': '1',
                'columns_duplication': '',
                'ordinal': '1',
                'dict_ordinal_encoding': '',
                'encoding':'1',
                'scaling': '0' if scaling != 'vanilla' else '1',
                'scaling_type': scaling,
            }

            payload = preprocess.handle(**preproc_kwargs)

            serializer = DatasetSerializer(data=payload)
            if serializer.is_valid():
                scaled_dataset = serializer.save()

                for algorithm in algorithms[self.method]:
                    model_payload = {
                        'name': f"{scaling}_{algorithm}_{self.name}",
                        'dataset': scaled_dataset,
                        'method': self.method,
                        'algorithm': algorithm,
                        'feature': self.feature,
                        'target': self.target,
                        'autoML_project': self,
                    }

                    serializer = AutoMLModelSerializer(data=model_payload)
                    if serializer.is_valid():
                        model = serializer.save()

                        model.initiate_training()

                        models_generated.append(model)

        return AutoMLModelSerializer(models_generated, many=True)
