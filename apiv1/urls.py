from django.urls import path
from apiv1.views import AvailableClassesListAPIView, StudentsFromClassAPIView, MyInfoAPIView


urlpatterns = [
    path('classes/', AvailableClassesListAPIView.as_view()),
    path('classes/<uuid:class_id>/students/', StudentsFromClassAPIView.as_view()),
    path('auth/me/', MyInfoAPIView.as_view())
]
