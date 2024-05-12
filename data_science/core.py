import json

import pandas as pd
from typing import Tuple, Dict
from pandas.core.frame import DataFrame


class DataScience:
    
    dataframe = None

    def __init__(self, dataframe: DataFrame) -> None:
        self.dataframe = dataframe

    def get_dataframe_shape(self) -> Tuple[int, int]:
        return self.dataframe.shape

    def get_all_column_type(self) -> Dict[str, str]:
        column_data_type = self.dataframe.dtypes
        key = column_data_type.index.to_list()
        value = ['Numerical' if v in ['int64', 'float64'] else 'Non-Numerical' for v in map(str,list(column_data_type.values))]

        return dict(zip(key, value))

    def get_numeric_and_non_numeric_columns(self):
        columns_type = self.get_all_column_type()
        numeric_type = []
        non_numeric_type = []
        for k, v in columns_type.items():
            if v in ['Numerical']:
                numeric_type.append(k)
            else:
                non_numeric_type.append(k)
        numeric = ''
        non_numeric = ''
        if len(numeric_type) != 0:
            numeric = ','.join(numeric_type)
        if len(non_numeric_type) != 0:
            non_numeric = ','.join(non_numeric_type)

        return numeric, non_numeric

    def get_preview(self, page, rows_per_page):
        max_row = self.dataframe.shape[0]
        first_row = (page - 1) * rows_per_page
        last_row = first_row + rows_per_page
        if last_row > max_row:
            last_row = max_row

        return json.loads(self.dataframe.iloc[first_row:last_row].to_json())
