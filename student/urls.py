from django.urls import path

from student.views import UploadStudentsExcelView

app_name = 'student'

urlpatterns = [
    path('upload/', UploadStudentsExcelView.as_view(), name='upload'),
]
