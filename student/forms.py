from django.forms import ModelForm

from student.models import StudentExel


class StudentExcelUploadForm(ModelForm):

    class Meta:
        model = StudentExel
        fields = ('excel_file', )
