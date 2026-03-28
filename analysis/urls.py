from django.urls import path
from .views import analysis_dashboard, trigger_analysis, check_status, upload_screenshot

urlpatterns = [
    path('analysis/', analysis_dashboard, name='analysis_dashboard'),
    path('trigger/', trigger_analysis, name='trigger_analysis'),
    path('status/<int:pk>/', check_status, name='check_status'),
    path('upload/', upload_screenshot, name='upload_screenshot'),
]