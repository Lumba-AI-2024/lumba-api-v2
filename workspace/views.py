from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from workspace.models import Workspace
from workspace.serializers import WorkspaceSerializer


# Create your views here.
class WorkspaceList(APIView):
    """
    List all workspace
    """
    def get(self, request):
        workspaces = Workspace.objects.all()
        serializer = WorkspaceSerializer(workspaces, many=True)
        return Response(serializer.data)

class WorkspaceDetail(APIView):
    """
    Create, Read, Update, and Delete workspaces
    """
    def get_workspace(self, name):
        try:
            return Workspace.objects.get(name=name)
        except Workspace.DoesNotExist:
            raise Http404

    def get(self, request):
        workspace = self.get_workspace(request.query_params['name'])
        serializer = WorkspaceSerializer(workspace)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = WorkspaceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        workspace = self.get_workspace(request.query_params['name'])
        serializer = WorkspaceSerializer(workspace, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        workspace = self.get_workspace(request.data['name'])
        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
