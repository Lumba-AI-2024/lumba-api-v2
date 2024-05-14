from django.urls import path
from .views import MLModelListView, MLModelDetailView, model_do_predict

urlpatterns = [
    path('list/', MLModelListView.as_view()),
    path('', MLModelDetailView.as_view()),
    path('predict/', model_do_predict),
]