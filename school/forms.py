from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q

from accounts.models import CustomUser
from school.models import School, Class


class CreateSchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name']


class CreateUpdateClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = ('name', )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CreateUpdateClassForm, self).__init__(*args, **kwargs)

    def clean_name(self, value):
        name = value
        if Class.objects.filter(Q(name=name) & Q(school=self.user.school)).count() > 0:
            raise ValidationError("Class " + name + " already exists")

    def save(self, commit=True):
        new_class = super(CreateUpdateClassForm, self).save(commit=False)
        new_class.school = self.user.form
        if self.user.role == CustomUser.Roles.TEACHER:
            new_class.teachers.add(self.user)
        if commit:
            new_class.save()
        return new_class


