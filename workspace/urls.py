from django.urls import path

from workspace.views import WorkspaceList, WorkspaceDetail

urlpatterns = [
    path('', WorkspaceDetail.as_view()),
    path('list/', WorkspaceList.as_view()),
]