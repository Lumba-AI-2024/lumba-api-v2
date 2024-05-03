from django.urls import path
from .views import MLModelListView, MLModelDetailView, model_do_predict

urlpatterns = [
    # DONE
    path('list/', MLModelListView.as_view()),
    path('', MLModelDetailView.as_view()),
    path('predict/', model_do_predict),
    # -------------------------------

    # path('initiate/', initiate_modeling),
    # path('save/', save_model),
    # TODO: jadiin 1 endpoint aja tapi beda method (/record)

    # path('createrecord/', create_training_record),
    # path('updaterecord/', update_training_record),
    # path('getrecord/', get_training_record),



]