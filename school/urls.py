from django.urls import path

from school import views

urlpatterns = [
    path('', views.school_list, name='school-list'),
    path('school-create/', views.school_create, name='school-create'),
    path('school-update/<uuid:pk>/', views.school_create, name='school-update'),
]
