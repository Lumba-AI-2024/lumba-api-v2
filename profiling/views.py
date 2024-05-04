import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

from data_cleaning_endpoint.checking_views import get_dataset
from data_science.analysis import Analysis
import os

@api_view()
def get_bar_chart(request):
    try:
        file_name = request.query_params['filename']
        username = request.query_params['username']
        workspace = request.query_params['workspace']
    except:
        return Response({'message': "input error"},status=status.HTTP_400_BAD_REQUEST)

    dataset = get_dataset(filename=file_name, workspace=workspace, username=username)
    dataframe = pd.read_csv(dataset.file)
    profiling = Analysis(dataframe=dataframe)
    result = json.loads(profiling.get_bar_chart_data())
    return Response(result,status=status.HTTP_200_OK)

@api_view()
def get_data_describe(request):
    try:
        file_name = request.query_params['filename']
        username = request.query_params['username']
        workspace = request.query_params['workspace']
    except:
        return Response({'message': "input error"},status=status.HTTP_400_BAD_REQUEST)

    dataset = get_dataset(filename=file_name, workspace=workspace, username=username)
    dataframe = pd.read_csv(dataset.file)
    profiling = Analysis(dataframe=dataframe)
    result = json.loads(profiling.get_data_describe())
    return Response(result,status=status.HTTP_200_OK)
