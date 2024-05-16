import json

import pandas

from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response

from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler

from dataset.models import Dataset
from dataset.serializers import DatasetSerializer

    def __init__(self, dataset: Dataset, columns: list = None) -> None:
        dataframe = pandas.read_csv(dataset.file)
        self.columns = columns or []
        print(f"This is in Preproc -> {columns}")
        self.target = dataset

    def handle(self, filename_prefix='preprocessed', **kwargs):
        if kwargs['missing'] == '1':
            if kwargs['columns_missing'] != '':
                col = kwargs['columns_missing'].split(",")
                self.data_null_handler(col)
            else:
                self.data_null_handler()

        if kwargs['duplication'] == '1':
            if kwargs['columns_duplication'] != '':
                col = kwargs['columns_duplication'].split(",")
                self.data_duplication_handler(col)
            else:
                self.data_duplication_handler()

        if kwargs['outlier'] == '1':
            self.data_outlier_handler()

        if kwargs['ordinal'] == '1':
            if kwargs['dict_ordinal_encoding'] != '':
                result_dict = json.loads(kwargs['dict_ordinal_encoding'])
                self.data_ordinal_encoding(result_dict)
            else:
                self.data_ordinal_encoding()

        if kwargs['encoding'] == '1':
            self.data_encoding()

        if kwargs['scaling'] == '1':
            if kwargs['scaling_type'] == 'normalization':
                self.data_normalization()
            else:
                self.data_standardization()

        new_file_name = f"{filename_prefix}_{self.target.name}"
        new_file_content = self.dataframe.to_csv()
        new_file = ContentFile(new_file_content.encode('utf-8'), name=new_file_name)

        # create new file model with serializer
        file_size = round(new_file.size / (1024 * 1024), 2)

        # check and collect columns type
        numeric, non_numeric = self.get_numeric_and_non_numeric_columns()
        workspace = self.target.workspace.pk

        payload = {
            'file': new_file,
            'name': new_file_name,
            'size': file_size,
            'username': self.target.username,
            'workspace': workspace,
            'numeric': numeric,
            'non_numeric': non_numeric,
        }

        return payload

    def data_standardization(self) -> DataFrame:
        df = self.dataframe.copy()
        # use standard scaler from sklearn and just use .fit
        scaler = StandardScaler()
        scaler.fit(df)

        self.dataframe = df

        return df

    def data_normalization(self) -> DataFrame:

        # use min-max scaler from sklearn and just use .fit
        scaler = MinMaxScaler()
        scaler.fit(df)

        self.dataframe = df

        return df

    def data_null_check(self) -> Dict[str, int]:
        df = self.dataframe[self.columns].copy()
        df = self.dataframe[self.columns].copy()
        df = self.dataframe[self.columns].copy()
        df = self.dataframe[self.columns].copy()
        df = self.dataframe[self.columns].copy()
        df = self.dataframe[self.columns].copy()
        df = self.dataframe[self.columns].copy()
    