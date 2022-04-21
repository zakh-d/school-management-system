from django.urls import path

from school import views

urlpatterns = [
    path('', views.school_list, name='school-list'),
    path('school-create/', views.school_create, name='school-create'),
    path('school-update/<uuid:pk>/', views.school_update, name='school-update'),
    path('school-delete/<uuid:pk>/', views.school_delete, name='school-delete'),
]
