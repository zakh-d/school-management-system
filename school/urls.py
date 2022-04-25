from django.urls import path
from school import views

urlpatterns = [
    path('create/', views.CreateSchoolView.as_view(), name='school-create'),
    path('update/<uuid:pk>/', views.UpdateSchoolView.as_view(), name='school-update'),
    path('class/create/', views.ClassCreateView.as_view(), name="class_create"),
    path('class/<uuid:pk>/', views.ClassDetailView.as_view(), name="class_detail")
]
