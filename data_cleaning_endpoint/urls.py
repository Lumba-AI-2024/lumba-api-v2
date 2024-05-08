from django.urls import path, re_path
from .views import null_check, duplication_check, outlier_check, cleaning_handler, get_boxplot

urlpatterns = [
    path('null/', null_check),
    path('duplication/', duplication_check),
    path('outlier/', outlier_check),
    path('handle/', cleaning_handler),
    path('boxplot/', get_boxplot),
]