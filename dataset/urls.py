from django.urls import path

from dataset.views import DatasetDetail, DatasetList

urlpatterns = [
    path('', DatasetDetail.as_view()),
    path('list/', DatasetList.as_view())
]