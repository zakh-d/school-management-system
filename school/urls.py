from django.urls import path
from school import views

app_name = 'school'

urlpatterns = [
    path('create/', views.CreateSchoolView.as_view(), name='create_school'),
    path('update/<uuid:pk>/', views.UpdateSchoolView.as_view(), name='update_school'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('class/create/', views.ClassCreateView.as_view(), name="class_create"),
    path('class/<uuid:pk>/', views.ClassDetailView.as_view(), name="class_detail"),
    path('class/add-teacher-not-public/<uuid:id>/', views.class_add_teacher_handler, name="add_teacher"),
    path('update-classes-not-public/<uuid:school_id>', views.increase_classes_number_handler, name="increase_class"),
]
