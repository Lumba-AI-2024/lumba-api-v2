from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
        print(serializer)
        return Response(serializer.data)


class DatasetDetail(APIView):
    def get_dataset(self, filename):
        try:
            return Dataset.objects.get(name=filename)
        except Dataset.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = DatasetSerializer(data={
            **request.data.dict(),
            'size': round(request.data['file'].size / (1024 * 1024), 2),
            'name': request.data['file'].name,
        })
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({**serializer.data},
                            status=status.HTTP_201_CREATED)
        # TODO: implement numerical and non numerical field
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # TODO: Implement this
        """
        This will generate preview of the file
        :param request:
        :return:
        """
        pass

    def put(self, request):
        dataset = self.get_dataset(request.query_params['oldfilename'])

        serializer = DatasetSerializer(dataset, {'name': request.data['newfilename']}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        dataset = self.get_dataset(request.data['filename'])
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
