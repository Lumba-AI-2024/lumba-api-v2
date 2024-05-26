from django.urls import path
from .views import MLModelListView, MLModelDetailView, model_do_predict, AutoMLModelListView, MLModelRetrainView

urlpatterns = [
    path('list/', MLModelListView.as_view()),
    path('', MLModelDetailView.as_view()),
    path('predict/', model_do_predict),
    path('listauto/', AutoMLModelListView.as_view()),
    path('retrain/', MLModelRetrainView.as_view())
]