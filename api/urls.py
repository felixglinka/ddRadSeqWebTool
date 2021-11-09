from django.urls import path

from . import views
from .views import FastaFileUploadCompleteView, FastaFileUploadView

urlpatterns = [
    path('', views.webinterfaceViews, name='main'),
    path('api/chunked_upload/', FastaFileUploadView.as_view(), name='api_chunked_upload'),
    path('api/chunked_upload_complete/', FastaFileUploadCompleteView.as_view(), name='api_chunked_upload_complete'),
    path('explanation', views.explanationsViews, name='explanation'),
]
