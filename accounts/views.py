from django.shortcuts import render
from django.views import generic
from accounts.forms import TeacherCreationForm, SchoolAdminCreationForm
from accounts.models import CustomUser


class TeacherSignUpView(generic.CreateView):

    model = CustomUser
    form_class = TeacherCreationForm
    template_name = "registration/signup.html"


class SchoolAdminSignUpView(generic.CreateView):

    model = CustomUser
    form_class = SchoolAdminCreationForm
    template_name = "registration/signup.html"
