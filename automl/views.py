from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from automl.models import AutoML
from automl.serializers import AutoMLSerializer
from dataset.models import Dataset
from workspace.models import Workspace


# Create your views here.
class AutoMLListView(APIView):
    def get(self, request):
        workspace = Workspace.objects.get(name=request.query_params['workspace'],
                                          username=request.query_params['username'])
        datasets = Dataset.objects.filter(workspace=workspace)
        automls = AutoML.objects.filter(dataset__in=datasets)
        serializer = AutoMLSerializer(automls, many=True)
        return Response(serializer.data)


def get_automl(automlname, datasetname, workspace, username):
    try:
        _workspace = Workspace.objects.get(name=workspace, username=username)
        dataset = Dataset.objects.get(workspace=_workspace, username=username, name=datasetname)
        try:
            return AutoML.objects.get(dataset=dataset, name=automlname)
        except AutoML.MultipleObjectsReturned:
            return AutoML.objects.filter(dataset=dataset, name=automlname)
    except (Workspace.DoesNotExist, AutoML.DoesNotExist):
        raise Http404


class AutoMLDetailView(APIView):
    def get(self, request):
        """
        Use workspace name, username, and model name to get the data for THAT model status
        :param request:
        :return:
        """
        automl_project = get_automl(
            automlname=request.query_params['automlname'],
            datasetname=request.query_params['datasetname'],
            workspace=request.query_params['workspace'],
            username=request.query_params['username']
        )
        serializer = AutoMLSerializer(automl_project)
        return Response(serializer.data)

    def put(self, request):
        """
        Update the status field of queried model
        :param request: params: modelname, workspace, username; data: status
        :return:
        """
        automl_project = get_automl(
            automlname=request.query_params['automlname'],
            datasetname=request.query_params['datasetname'],
            workspace=request.query_params['workspace'],
            username=request.query_params['username']
        )
        serializer = AutoMLSerializer(automl_project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        datasetname:
        username:
        workspace:
        automlname:
        method:
        feature:
        target:
        ordinal:
        ordinal_dict:
        :return:
        """
        workspace = Workspace.objects.get(username=request.data['username'], name=request.data['workspace'])
        dataset = Dataset.objects.get(name=request.data['datasetname'], workspace=workspace,
                                      username=request.data['username'])
        payload = {**request.data.dict(), 'dataset': dataset.pk, 'name': request.data['automlname']}
        serializer = AutoMLSerializer(data=payload)
        if serializer.is_valid():
            automl_project = serializer.save()
            automl_project.initiate_project()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        automl_project = get_automl(
            automlname=request.data['automlname'],
            datasetname=request.data['datasetname'],
            workspace=request.data['workspace'],
            username=request.data['username']
        )
        automl_project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AutoMLRetrainView(APIView):
    def post(self, request):
        automl_project = get_automl(
            automlname=request.query_params['automlname'],
            datasetname=request.query_params['datasetname'],
            workspace=request.query_params['workspace'],
            username=request.query_params['username']
        )

        automl_project.retrain_all()

        return Response(status=status.HTTP_200_OK)

