from django.urls import path
from .views import AutoMLListView, AutoMLDetailView, AutoMLRetrainView

urlpatterns = [
    path('list/', AutoMLListView.as_view()),
    path('', AutoMLDetailView.as_view()),
    path('retrain/', AutoMLRetrainView.as_view())
]