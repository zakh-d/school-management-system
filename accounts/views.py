from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic
from accounts.forms import TeacherCreationForm, SchoolAdminCreationForm, LoginForm
from accounts.models import CustomUser
from config.settings import LOGIN_REDIRECT_URL


class TeacherSignUpView(generic.CreateView):

    model = CustomUser
    form_class = TeacherCreationForm
    template_name = "registration/signup.html"


class SchoolAdminSignUpView(generic.CreateView):

    model = CustomUser
    form_class = SchoolAdminCreationForm
    template_name = "registration/signup.html"


class ProfileView(LoginRequiredMixin, generic.TemplateView):

    template_name = "registration/profile.html"

    def get_context_data(self, **kwargs):

        return {'user': self.request.user}


def login_view(request):

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username_or_email, password=password)
            if user:
                login(request, user)
                return redirect(LOGIN_REDIRECT_URL)
            return render(request, 'registration/login.html', {'form': form, 'error': True})
    return render(request, 'registration/login.html', {'form': form})
