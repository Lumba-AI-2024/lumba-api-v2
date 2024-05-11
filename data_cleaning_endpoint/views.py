import json
import random
import string

from django.core.files.base import ContentFile
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from data_science.preprocess import Preprocess
from data_science.analysis import Analysis
import os

from dataset.models import Dataset
from dataset.serializers import DatasetSerializer
from dataset.views import get_dataset
from workspace.models import Workspace




@api_view()
def null_check(request):
    dataset = get_dataset(
        filename=request.query_params['filename'],
        workspace=request.query_params['workspace'],
        username=request.query_params['username'],
        workspace_type=request.query_params['type']
    )
    dataframe = pd.read_csv(dataset.file)
    preproceess = Preprocess(dataframe=dataframe)
    result = preproceess.data_null_check()
    return Response(result,status=status.HTTP_200_OK)

@api_view()
def duplication_check(request):
    dataset = get_dataset(
        filename=request.query_params['filename'],
        workspace=request.query_params['workspace'],
        username=request.query_params['username'],
        workspace_type=request.query_params['type']
    )
    dataframe = pd.read_csv(dataset.file)
    preproceess = Preprocess(dataframe=dataframe)
    result = preproceess.data_duplication_check()
    return Response(result,status=status.HTTP_200_OK)

@api_view()
def outlier_check(request):
    dataset = get_dataset(
        filename=request.query_params['filename'],
        workspace=request.query_params['workspace'],
        username=request.query_params['username'],
        workspace_type=request.query_params['type']
    )
    dataframe = pd.read_csv(dataset.file)
    preproceess = Preprocess(dataframe=dataframe)
    result = preproceess.data_outlier_check()
    return Response(result,status=status.HTTP_200_OK)

@api_view()
def get_boxplot(request):
    dataset = get_dataset(
        filename=request.query_params['filename'],
        workspace=request.query_params['workspace'],
        username=request.query_params['username'],
        workspace_type=request.query_params['type']
    )
    dataframe = pd.read_csv(dataset.file)
    analysis = Analysis(dataframe=dataframe)
    result = json.loads(analysis.get_box_plot_data())
    return Response(result,status=status.HTTP_200_OK)

@api_view()
def encode_check(request):
    dataset = get_dataset(
        filename=request.query_params['filename'],
        workspace=request.query_params['workspace'],
        username=request.query_params['username'],
        workspace_type=request.query_params['type']
    )
    dataframe = pd.read_csv(dataset.file)
    preproceess = Preprocess(dataframe=dataframe)
    result = preproceess.data_encode_check()
    return Response(result,status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def cleaning_handler(request):
    try:
        file_name = request.data['filename']
        username = request.data['username']
        workspace = request.data['workspace']
        workspace_type = request.data['type']
    except:
        return Response({'message': "input error"}, status=status.HTTP_400_BAD_REQUEST)

    dataset = get_dataset(
        filename=request.data['filename'],
        workspace=request.data['workspace'],
        username=request.data['username'],
        workspace_type=request.data['type']
    )
    dataframe = pd.read_csv(dataset.file)
    preprocess = Preprocess(dataframe=dataframe)
    
    if request.data['missing'] == '1':
        if request.data['columns_missing'] != '':
            col = request.data['columns_missing'].split(",")
            preprocess.data_null_handler(col)
        else:
            preprocess.data_null_handler()

    if request.data['duplication'] == '1':
        if request.data['columns_duplication'] != '':
            col = request.data['columns_duplication'].split(",")
            preprocess.data_duplication_handler(col)
        else:
            preprocess.data_duplication_handler()

    if request.data['outlier'] == '1':
        preprocess.data_outlier_handler()

    # generate new file name
    # TODO: rename with proper preprocess method
    new_file_name = generate_file_name(file_name)
    new_file_content = preprocess.dataframe.to_csv()
    new_file = ContentFile(new_file_content.encode('utf-8'), name=new_file_name)

    # create new file model with serializer
    file_size = round(new_file.size / (1024 * 1024), 2)

    # check and collect columns type
    numeric, non_numeric = preprocess.get_numeric_and_non_numeric_columns()
    workspace_obj = Workspace.objects.get(name=workspace, username=username, type=workspace_type)
    workspace_pk = workspace_obj.pk

    payload = {
        'file': new_file,
        'name': new_file_name,
        'size': file_size,
        'username': username,
        'workspace': workspace_pk,
        'numeric': numeric,
        'non_numeric': non_numeric,
    }
    serializer = DatasetSerializer(data=payload)
    if serializer.is_valid():
        serializer.save()
        return Response(preprocess.get_preview(1, 10), status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_file_name(file_name):
    _file, ext = os.path.splitext(file_name)
    new_file_name = _file + "_" + random_string() + ext
    return new_file_name


def random_string(length=4):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
