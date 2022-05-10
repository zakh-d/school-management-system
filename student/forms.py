from django.forms import forms
from django.core.validators import FileExtensionValidator


class StudentExcelUploadForm(forms.Form):

    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['xlsx'])],
                           help_text='Attach .xlsx file', label='File')
