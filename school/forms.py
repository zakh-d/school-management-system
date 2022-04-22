from django import forms

from school.models import School


class CreateSchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name']
