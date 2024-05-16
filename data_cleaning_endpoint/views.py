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
        datasetname=request.query_params['datasetname'],
        workspace=request.query_params['workspace'],
        username=request.query_params['username'],
        workspace_type=request.query_params['type']
    )
    if 'selected_columns' not in request.query_params:
        preproceess = Preprocess(dataset=dataset)
        result = preproceess.data_duplication_check()
        return Response(result, status=status.HTTP_200_OK)
    columns = request.query_params['selected_columns']
    columns = columns.split(",")
    dataframe = pd.read_csv(dataset.file)
    preproceess = Preprocess(dataframe=dataframe, columns=columns)
    result = preproceess.data_null_check()
    return Response(result, status=status.HTTP_200_OK)


@api_view()
def duplication_check(request):
    dataset = get_dataset(
        datasetname=request.query_params['datasetname'],
        workspace=request.query_params['workspace'],
        username=request.query_params['username'],
        workspace_type=request.query_params['type']
    )
    if 'selected_columns' not in request.query_params:
        dataframe = pd.read_csv(dataset.file)
        preproceess = Preprocess(dataframe=dataframe)
        result = preproceess.data_duplication_check()
        return Response(result, status=status.HTTP_200_OK)
    columns = request.query_params['selected_columns']
    columns = columns.split(",")
    dataframe = pd.read_csv(dataset.file)
    preproceess = Preprocess(dataframe=dataframe, columns=columns)
    result = preproceess.data_duplication_check()
    return Response(result, status=status.HTTP_200_OK)


@api_view()
def outlier_check(request):
    dataset = get_dataset(
        datasetname=request.query_params['datasetname'],
        workspace=request.query_params['workspace'],
        username=request.query_params['username'],
        workspace_type=request.query_params['type']
    )
    preproceess = Preprocess(dataset=dataset)
    result = preproceess.data_outlier_check()
    return Response(result, status=status.HTTP_200_OK)


@api_view()
def get_boxplot(request):
    dataset = get_dataset(
        datasetname=request.query_params['datasetname'],
        workspace=request.query_params['workspace'],
        username=request.query_params['username'],
        workspace_type=request.query_params['type']
    )
    dataframe = pd.read_csv(dataset.file)
    analysis = Analysis(dataframe=dataframe)
    result = json.loads(analysis.get_box_plot_data())
    return Response(result, status=status.HTTP_200_OK)


@api_view()
def encode_check(request):
    dataset = get_dataset(
        datasetname=request.query_params['datasetname'],
        workspace=request.query_params['workspace'],
        username=request.query_params['username'],
        workspace_type=request.query_params['type']
    )
    if 'selected_columns' not in request.query_params:
        preproceess = Preprocess(dataset=dataset)
        result = preproceess.data_duplication_check()
        return Response(result, status=status.HTTP_200_OK)
    columns = request.query_params['selected_columns']
    columns = columns.split(",")
    preproceess = Preprocess(dataset=dataset, columns=columns)
    result = preproceess.data_encode_check()
    return Response(result, status=status.HTTP_200_OK)


@api_view()
def filter_data(request):
    dataset = get_dataset(
        datasetname=request.query_params['datasetname'],
        workspace=request.query_params['workspace'],
        username=request.query_params['username'],
        workspace_type=request.query_params['type']
    )
    preproceess = Preprocess(dataset=dataset)
    # tambah list as a parameter
    result = preproceess.data_column_filter()
    return Response(result,status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def cleaning_handler(request):
    dataset = get_dataset(
        datasetname=request.data['datasetname'],
        workspace=request.data['workspace'],
        username=request.data['username'],
        workspace_type=request.data['type']
    )
    preprocess = Preprocess(dataset=dataset)
    print(request.data.dict())
    payload = preprocess.handle(**request.data.dict())

    serializer = DatasetSerializer(data=payload)
    if serializer.is_valid():
        serializer.save()
        return Response(preprocess.get_preview(1, 10), status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
def cleaning_automl(request):
    print(request.data)
    try:
        file_name = request.data['datasetname']
        username = request.data['username']
        workspace = request.data['workspace']
        workspace_type = request.data['type']
    except:
        return Response({'message': "input error"}, status=status.HTTP_400_BAD_REQUEST)

    dataset = get_dataset(
        datasetname=request.data['datasetname'],
        workspace=request.data['workspace'],
        username=request.data['username'],
        workspace_type=request.data['type']
    )
    columns=request.data['selectedTrainingColumns']
    columns = columns.split(",")
    preprocess = Preprocess(dataset=dataset, columns=columns)
    
    # preprocess
    preprocess.data_null_handler()
    preprocess.data_duplication_handler()
    
    # handle ordinal encoding
    if request.data['ordinal'] == '1':
        if request.data['dict_ordinal_encoding'] != '':
            result_dict = json.loads(request.data['dict_ordinal_encoding'])
            preprocess.data_ordinal_encoding(result_dict)
        else:
            preprocess.data_ordinal_encoding()
    
    # handle encoding
    # kolom = []
    # if request.args.get('encoding') == '1':
    #     if request.args.get('columns_encoding') != '':
    #         col = request.args.get('columns_encoding').split(",")
    #         kolom = col
    #         preprocess.data_encoding(col)
    #     else:
    #         preprocess.data_encoding()

    preprocess.data_encoding()

    new_file_name = generate_file_name_automl(file_name)
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


def generate_file_name_automl(file_name):
    _file, ext = os.path.splitext(file_name)
    new_file_name = _file + "_preprocess" + ext
    return new_file_name


def random_string(length=4):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
