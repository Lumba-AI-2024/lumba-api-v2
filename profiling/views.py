import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

from data_science.analysis import Analysis
import os

from data_science.utils import info_per_columns
from dataset.views import get_dataset


@api_view()
def get_bar_chart(request):
    try:
        file_name = request.query_params['filename']
        username = request.query_params['username']
        workspace = request.query_params['workspace']
        workspace_type = request.query_params['type']
    except:
        return Response({'message': "input error"},status=status.HTTP_400_BAD_REQUEST)

    dataset = get_dataset(filename=file_name, workspace=workspace, username=username, workspace_type=workspace_type)
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
        workspace_type = request.query_params['type']
    except:
        return Response({'message': "input error"},status=status.HTTP_400_BAD_REQUEST)

    dataset = get_dataset(filename=file_name, workspace=workspace, username=username, workspace_type=workspace_type)
    dataframe = pd.read_csv(dataset.file)
    profiling = Analysis(dataframe=dataframe)
    result = json.loads(profiling.get_data_describe())
    return Response(result,status=status.HTTP_200_OK)

@api_view()
def get_info_per_column(request):
    try:
        file_name = request.query_params['filename']
        username = request.query_params['username']
        workspace = request.query_params['workspace']
        workspace_type = request.query_params['type']
    except:
        return Response({'message': "input error"},status=status.HTTP_400_BAD_REQUEST)

    dataset = get_dataset(filename=file_name, workspace=workspace, username=username, workspace_type=workspace_type)
    dataframe = pd.read_csv(dataset.file)
    result = info_per_columns(dataframe) # KEnapa jadi 1 sama class analysis????????? TODO: refactor
    return Response(result,status=status.HTTP_200_OK)