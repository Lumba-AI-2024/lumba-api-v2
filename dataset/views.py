import json

import pandas
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from data_science.core import DataScience
from dataset.models import Dataset
from dataset.serializers import DatasetSerializer
from workspace.models import Workspace


# Create your views here.
class DatasetList(APIView):
    def get(self, request):
        workspace = Workspace.objects.get(name=request.query_params['workspace'])
        datasets = Dataset.objects.filter(
            username=request.query_params['username'],
            workspace=workspace
        )
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)


class DatasetDetail(APIView):
    def get_dataset(self, filename, workspace, username):
        try:
            _workspace = Workspace.objects.get(name=workspace, username=username)
            return Dataset.objects.get(name=filename, workspace=_workspace, username=username)
        except Dataset.DoesNotExist:
            raise Http404

    def post(self, request):
        # Not touching this. Just copied and pasted from what's coded previously
        # This SHOULD be a method in DataScience class
        df = pandas.read_csv(request.data['file'].file)
        ds = DataScience(dataframe=df)
        numeric, non_numeric = ds.get_numeric_and_non_numeric_columns()
        serializer = DatasetSerializer(data={
            **request.data.dict(),
            'size': round(request.data['file'].size / (1024 * 1024), 2),
            'name': request.data['file'].name,
            'numeric': numeric,
            'non_numeric': non_numeric,
        })
        if serializer.is_valid():
            serializer.save()
            return Response({**serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            file_name = request.query_params['filename']
            username = request.query_params['username']
            workspace = request.query_params['workspace']
        except:
            return Response({'message': "input error"}, status=status.HTTP_400_BAD_REQUEST)

        dataframe = pandas.read_csv(self.get_dataset(filename=file_name, username=username, workspace=workspace).file)

        ds = DataScience(dataframe)

        return Response(ds.get_preview(int(request.query_params['page']), int(request.query_params['rowsperpage'])), status=status.HTTP_200_OK)

    def put(self, request):
        dataset = self.get_dataset(request.query_params['oldfilename'], request.query_params['workspace'], request.query_params['username'])

        serializer = DatasetSerializer(dataset, {'name': request.data['newfilename']}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        dataset = self.get_dataset(request.data['filename'], request.data['workspace'], request.data['username'])
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
