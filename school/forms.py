from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from accounts.models import Teacher
from school.models import School, Class


class CreateSchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name']


class CreateUpdateClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = ('name', )

    def __init__(self, school, *args, **kwargs):
        super(CreateUpdateClassForm, self).__init__(*args, **kwargs)
        self.school = school

    def clean_name(self):
        name = self.cleaned_data['name']
        if Class.objects.filter(Q(name=name) & Q(school=self.school)).exists():
            raise ValidationError("Class " + name + " already exists")
        return name


class AddTeacherClassForm(forms.ModelForm):

    def __init__(self, school=None, *args, **kwargs):
        super(AddTeacherClassForm, self).__init__(*args, **kwargs)
        if school:
            self.fields['teachers'].queryset = Teacher.objects.filter(school=school)

    class Meta:
        model = Class
        fields = ('teachers', )
