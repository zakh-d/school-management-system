from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import AdministrationMember, Teacher
from school.models import School


class TeacherCreationForm(UserCreationForm):

    school_id = forms.UUIDField(label='School ID')

    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def clean_school_id(self):

        try:
            School.objects.get(pk=self.cleaned_data.get('school_id'))
        except School.DoesNotExist:
            self.add_error('school_id', 'School with given id does not exist')
        return self.cleaned_data.get('school_id')

    def save(self, commit=True):

        teacher = super(TeacherCreationForm, self).save(commit=False)
        teacher.school = School.objects.get(pk=self.cleaned_data.get('school_id'))

        if commit:
            teacher.save()  # Teacher model sets role TEACHER
        return teacher


class SchoolAdminCreationForm(UserCreationForm):

    class Meta:
        model = AdministrationMember
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        # AdministrationMember model sets role ADMIN_MEMBER on save


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email')


class LoginForm(forms.Form):

    username_or_email = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
