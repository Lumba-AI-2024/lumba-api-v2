from django.urls import path
from .views import AutoMLListView, AutoMLDetailView

urlpatterns = [
    path('list/', AutoMLListView.as_view()),
    path('', AutoMLDetailView.as_view()),
]