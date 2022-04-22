from django.urls import path
from school import views

urlpatterns = [
    path('', views.school_list, name='school-list'),
    path('create/', views.school_create, name='school-create'),
    path('update/<uuid:pk>/', views.school_update, name='school-update'),
    path('delete/<uuid:pk>/', views.school_delete, name='school-delete'),
]
