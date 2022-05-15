from django.urls import path
from apiv1.views import AvailableClassesListAPIView


urlpatterns = [
    path('classes/', AvailableClassesListAPIView.as_view())
]
