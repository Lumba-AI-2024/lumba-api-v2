import json
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from django.core.files.base import ContentFile
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from rest_framework import status
from rest_framework.response import Response
from data_science.core import DataScience
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from dataset.models import Dataset
from dataset.serializers import DatasetSerializer
import joblib

class Preprocess(DataScience):

    def __init__(self, dataset: Dataset, columns: list = None, target_columns: str = None) -> None:
        dataframe = pd.read_csv(dataset.file)
        super().__init__(dataframe)
        self.columns = columns or []
        self.target_columns = target_columns
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

        # if kwargs['outlier'] == '1':
        #     self.data_outlier_handler()

        if kwargs['ordinal'] == '1':
            if kwargs['dict_ordinal_encoding'] != '':
                result_dict = json.loads(kwargs['dict_ordinal_encoding'])
                self.data_ordinal_encoding(result_dict)
            # else:
            #     self.data_ordinal_encoding()

        if kwargs['encoding'] == '1':
            self.data_encoding()

        is_scaled = False
        if kwargs['scaling'] == '1':
            is_scaled = True
            if kwargs['scaling_type'] == 'normalization':
                scaler = self.data_normalization()
            else:
                scaler = self.data_standardization()
            
            # Save scaler to pkl file
            scaler_filename = f"{filename_prefix}_{self.target.name}_scaler.pkl"
            joblib.dump(scaler, scaler_filename)
            with open(scaler_filename, 'rb') as f:
                scaler_file = ContentFile(f.read(), name=scaler_filename)

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
            'scaler_file': scaler_file if is_scaled else None
        }

        print(payload)
        
        return payload

    def data_standardization(self) -> StandardScaler:
        df = self.dataframe.copy()
        if self.target_columns != '':
            features_to_scale = df.drop(columns=self.target_columns)
        else:
            features_to_scale = df
        
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features_to_scale)
        scaled_df = pd.DataFrame(scaled_features, columns=features_to_scale.columns)
        
        if self.target_columns != '':
            scaled_df[self.target_columns] = self.dataframe[self.target_columns].values
        
        self.dataframe = scaled_df
        
        return scaler

    def data_normalization(self) -> MinMaxScaler:
        df = self.dataframe.copy()
        if self.target_columns != '':
            features_to_scale = df.drop(columns=self.target_columns)
        else:
            features_to_scale = df
        
        scaler = MinMaxScaler()
        scaled_features = scaler.fit_transform(features_to_scale)
        scaled_df = pd.DataFrame(scaled_features, columns=features_to_scale.columns)
        
        if self.target_columns != '':
            scaled_df[self.target_columns] = self.dataframe[self.target_columns].values
        
        self.dataframe = scaled_df
        
        return scaler


    def data_null_check(self) -> Dict[str, int]:
        df = self.dataframe[self.columns].copy()
        total_null_for_each_column = dict(df.isnull().sum())

        return total_null_for_each_column

    def data_null_handler(self, columns: List[str]=None) -> DataFrame:
        df = self.dataframe[self.columns].copy()

        if columns != None:
            df.dropna(subset=columns, inplace=True)
        else:
            df.dropna(inplace=True)
            
        self.dataframe = df

        return df

    def data_duplication_check(self) -> int:
        df = self.dataframe[self.columns].copy()
        total_duplicate = df.duplicated().sum()

        return total_duplicate

    def data_duplication_handler(self, columns: List[str]=None) -> DataFrame:
        df = self.dataframe[self.columns].copy()

        if columns != None:
            df.drop_duplicates(subset=columns, inplace=True)
        else:
            df.drop_duplicates(inplace=True)

        self.dataframe = df

        return df

    def data_outlier_check(self) -> Dict[str, int]:
        """
        https://machinelearningmastery.com/how-to-use-statistics-to-identify-outliers-in-data/
        """
        df = self.dataframe.copy()
        total_outlier_for_each_column = dict()
        for col in df.columns:
            if df[col].dtype in ["int64", "float64"]:
                df_col_target = df[col]
                ul, ll = self._get_upper_lower_level(df_col_target)

                # get outliers only
                outliers = df_col_target[(df_col_target < ll) | (df_col_target > ul)]
                total_outlier_for_each_column[col] = len(outliers)

        return total_outlier_for_each_column

    def data_outlier_handler(self) -> DataFrame:
        df = self.dataframe.copy()

        all_outlier_rows_index = set()
        for col in df.columns:
            if df[col].dtype in ["int64", "float64"]:
                df_col_target = df[col]
                ul, ll = self._get_upper_lower_level(df_col_target)
                
                # exclude outliers from the data
                all_outlier_rows_index |= set(df_col_target[(df_col_target < ll) | (df_col_target > ul)].index)

        df = df.drop(list(all_outlier_rows_index), axis=0)
        self.dataframe = df

        return df
    
    def data_encode_check(self) -> Dict[str, List[str]]:
        df = self.dataframe[self.columns].copy()
        df.dropna(inplace=True)
        categorical_columns = dict()
        for col in df.columns:
            if df[col].dtype == "object":
                categorical_columns[col] = df[col].unique()
        
        return categorical_columns
    
    def data_column_filter(self, columns: List[str]) -> DataFrame:
        df = self.dataframe.copy()

        df = df[columns]

        self.dataframe = df

        return df
    
    def data_ordinal_encoding(self, mapping: Dict[str, Dict[str, int]]) -> DataFrame:
        df = self.dataframe[self.columns].copy()
        columns = mapping.keys()
        for col in columns:
            df[col] = df[col].map(mapping[col])

        self.dataframe = df

        return df
    # total row of dataframe
    def data_row(self) -> int:
        return len(self.dataframe)
    def data_encoding(self) -> DataFrame:
        df = self.dataframe[self.columns].copy()
        # df_feature = df.drop(columns=[self.target_columns])
        # df_target = df[self.target_columns]
        

        # df_feature = pd.get_dummies(df_feature)
        label = LabelEncoder()
        # for col in df_feature.columns:
        #     if len(df_feature[col].unique()) >= 2:
        #         df_feature[col] = label.fit_transform(df_feature[col])
                
        # df_target = label.fit_transform(df_target)
        # df_target = pd.DataFrame(df_target, columns=[self.target_columns])
        # print(type(df_target),"and",type(df_feature))
        # df = pd.concat([df_feature, df_target], axis=1)
        for col in df:
            if len(df[col].unique()) == 1:
                df.drop(col, axis=1, inplace=True)
        if self.target_columns != '':
            if df[self.target_columns].dtype == "object" :
                label = LabelEncoder()
                df[self.target_columns] = label.fit_transform(df[self.target_columns])
        for col in df.columns:
            if df[col].dtype == "object" and col != self.target_columns and len(df[col].unique()) == 2:
                label = LabelEncoder()
                df[col] = label.fit_transform(df[col])
            elif df[col].dtype == "object" and col != self.target_columns and len(df[col].unique()) > 2:
                df = pd.get_dummies(df, columns=[col])
        
        for col in df.columns:
            if col != self.target_columns and len(df[col].unique()) == 2:
                label = LabelEncoder()
                df[col] = label.fit_transform(df[col])
            
        self.dataframe = df
        print(f"This is in data_encoding -> {df}")

        return df
    
    @staticmethod
    def _get_upper_lower_level(df_col: Series) -> Tuple[float, float]:
        """
        This functions is used for handling outlier with IQR method
        """
        q1 = df_col.quantile(.25)
        q3 = df_col.quantile(.75)
        IQR = q3 - q1
        ll = q1 - (1.5*IQR)
        ul = q3 + (1.5*IQR)

        return ul, ll
                