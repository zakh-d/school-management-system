from django.urls import path

from student.views import UploadStudentsExcelView

app_name = 'student'

urlpatterns = [
    path('upload/<uuid:class_id>/', UploadStudentsExcelView.as_view(), name='upload'),
]
