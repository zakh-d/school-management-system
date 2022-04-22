from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from accounts.models import CustomUser
from school.models import School


class TeacherCreationForm(UserCreationForm):

    school_id = forms.UUIDField(label="School ID")

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def clean_school_id(self):

        try:
            School.objects.get(pk=self.cleaned_data.get('school_id'))
        except School.DoesNotExist:
            raise ValidationError("School with given id does not exist")
        return self.cleaned_data.get('school_id')

    def save(self, commit=True):

        teacher = super(TeacherCreationForm, self).save(commit=False)
        teacher.role = 0
        teacher.school = School.objects.get(pk=self.cleaned_data.get('school_id'))

        if commit:
            teacher.save()
        return teacher


class SchoolAdminCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):

        school_admin = super(SchoolAdminCreationForm, self).save(commit=False)
        school_admin.role = 1
        school_admin.school = None
        if commit:
            school_admin.save()
        return school_admin


class LoginForm(forms.Form):

    username_or_email = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
