from django.views import generic

from student.forms import StudentExcelUploadForm


class UploadStudentsExcelView(generic.CreateView):

    form_class = StudentExcelUploadForm
    template_name = 'student/upload.html'
