from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from dataset.models import Dataset
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


class MLModelDetailView(APIView):
    def get_model(self, modelname, workspace, username):
        try:
            _workspace = Workspace.objects.get(name=workspace, username=username)
            dataset = Dataset.objects.get(workspace=_workspace)
            return MLModel.objects.get(dataset=dataset)
        except (Workspace.DoesNotExist, MLModel.DoesNotExist):
            raise Http404

    def get(self, request):
        """
        Use workspace name, username, and model name to get the data for THAT model status
        :param request:
        :return:
        """
        model = self.get_model(
            request.query_params['modelname'],
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
        model = self.get_model(
            request.query_params['modelname'],
            request.query_params['workspace'],
            request.query_params['username']
        )
        serializer = MLModelSerializer(model, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        modelname:affairs
        filename:affairs.csv
        username:{{username}}
        workspace:{{workspace_name}}
        method:REGRESSION
        algorithm:LINEAR
        feature:rate_marriage,age,yrs_married,children,religious,educ,occupation,occupation_husb
        target:affairs
        :return:
        """
        workspace = Workspace.objects.get(username=request.data['username'], name=request.data['workspace'])
        dataset = Dataset.objects.get(name=request.data['filename'], workspace=workspace)

        serializer = MLModelSerializer(data={**request.data.dict(), 'dataset': dataset.pk, 'name':request.data['modelname']})
        if serializer.is_valid():
            serializer.save()
            try:
                # TODO: Commence training. Add implementation to the /train endpoint
                pass
            except:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_columns(request):
    pass