from django.urls import path

from school import views

app_name = 'school'

urlpatterns = [
    path('create/', views.CreateSchoolView.as_view(), name='create'),
    path('update/<uuid:pk>/', views.UpdateSchoolView.as_view(), name='update'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
