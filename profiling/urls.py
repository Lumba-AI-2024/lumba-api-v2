from django.urls import path, re_path

from profiling.views import get_bar_chart, get_info_per_column, get_data_describe

urlpatterns = [
    path('barchart/', get_bar_chart),
    path('describe/', get_data_describe),
    path('columninfo/', get_info_per_column),
]