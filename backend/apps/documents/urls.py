from django.urls import path
from .views import NextcloudSyncView

urlpatterns = [
    path("export-to-nextcloud/", NextcloudSyncView.as_view(), name="export_to_nextcloud"),
]
