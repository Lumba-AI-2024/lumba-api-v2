import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from data_science.core import DataScience

class Preprocess(DataScience):

    def __init__(self, dataframe: DataFrame) -> None:
        super().__init__(dataframe)

    def data_null_check(self) -> Dict[str, int]:
        df = self.dataframe.copy()
        total_null_for_each_column = dict(df.isnull().sum())

        return total_null_for_each_column

    def data_null_handler(self, columns: List[str]=None) -> DataFrame:
        df = self.dataframe.copy()

        if columns != None:
            df.dropna(subset=columns, inplace=True)
        else:
            df.dropna(inplace=True)
            
        self.dataframe = df

        return df

    def data_duplication_check(self) -> int:
        df = self.dataframe.copy()
        total_duplicate = df.duplicated().sum()

        return total_duplicate

    def data_duplication_handler(self, columns: List[str]=None) -> DataFrame:
        df = self.dataframe.copy()

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
                