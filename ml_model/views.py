import joblib as joblib
import numpy as np
from django.http import Http404
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from dataset.models import Dataset
from dataset.serializers import DatasetSerializer
from ml_model.models import MLModel
from ml_model.serializers import MLModelSerializer
from lumba_api_v2 import settings
from workspace.models import Workspace

# Create your views here.
training_service_url = settings.TRAINING_API_URL

class MLModelListView(APIView):
    def get(self, request):
        """
        :param request: {
        'params': {
            'username': username,
            'workspace': workspace
            }
        }
        """
        workspace = Workspace.objects.get(name=request.query_params['workspace'], username=request.query_params['username'])
        datasets = Dataset.objects.filter(workspace=workspace)
        mlmodels = MLModel.objects.filter(dataset__in=datasets)
        serializer = MLModelSerializer(mlmodels, many=True)
        return Response(serializer.data)


def get_model(modelname, datasetname, workspace, username):
    try:
        _workspace = Workspace.objects.get(name=workspace, username=username)
        dataset = Dataset.objects.get(workspace=_workspace, username=username, name=datasetname)
        return MLModel.objects.get(dataset=dataset, name=modelname)
    except (Workspace.DoesNotExist, MLModel.DoesNotExist):
        raise Http404


class MLModelDetailView(APIView):

    def get(self, request):
        """
        Use workspace name, username, and model name to get the data for THAT model status
        :param request:
        :return:
        """
        model = get_model(
            request.query_params['modelname'],
            request.query_params['datasetname'],
            request.query_params['workspace'],
            request.query_params['username']
        )
        serializer = MLModelSerializer(model)
        return Response(serializer.data)

    def put(self, request):
        """
        Update the status field of queried model
        :param request: params: modelname, workspace, username; data: status
        :return:
        """
        model = get_model(
            request.query_params['modelname'],
            request.query_params['datasetname'],
            request.query_params['workspace'],
            request.query_params['username']
        )
        print(request.data)
        serializer = MLModelSerializer(model, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        modelname:affairs
        datasetname:affairs.csv
        username:{{username}}
        workspace:{{workspace_name}}
        method:REGRESSION
        algorithm:LINEAR
        feature:rate_marriage,age,yrs_married,children,religious,educ,occupation,occupation_husb
        target:affairs
        :return:
        """
        print(request.data.dict())
        workspace = Workspace.objects.get(username=request.data['username'], name=request.data['workspace'])
        print(request.data['datasetname'],"test")
        dataset = Dataset.objects.get(name=request.data['datasetname'], workspace=workspace, username=request.data['username'])
        print("dataset",dataset)
        payload = {**request.data.dict(), 'dataset': dataset.pk, 'name': request.data['modelname']}
        serializer = MLModelSerializer(data=payload)
        if serializer.is_valid():
            model = serializer.save()
            return Response(model.initiate_training(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        model = get_model(
            modelname=request.data['modelname'],
            datasetname=request.data['datasetname'],
            workspace=request.data['workspace'],
            username=request.data['username']
        )
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def model_do_predict(request):
    """
    Not touching this because I don't understand what this does.
    :param request:
    :return:
    """
    try:
        model_name = request.query_params['modelname']
        feature = int(request.query_params['feature'])
        username = request.query_params['username']
        workspace = request.query_params['workspace']
    except:
        return Response({'message': "input error"}, status=status.HTTP_400_BAD_REQUEST)

    modelfile = get_model(model_name, workspace, username)
    model = joblib.load(modelfile.model_file.file)
    predict = model.predict(np.array([feature]).reshape(-1, 1))

    return Response({'result': predict[0][0]}, status=status.HTTP_200_OK)
