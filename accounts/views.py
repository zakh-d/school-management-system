from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.views import generic
from django.utils.http import urlsafe_base64_decode
from accounts.forms import TeacherCreationForm, SchoolAdminCreationForm, LoginForm
from accounts.models import CustomUser
from accounts.utils import send_activation_email, generate_token
from config.settings import LOGIN_REDIRECT_URL


class CustomUserSignUpView(generic.CreateView):

    model = CustomUser
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Send email after account created"""
        response = super(CustomUserSignUpView, self).form_valid(form)
        send_activation_email(self.object, self.request)
        return response


class TeacherSignUpView(CustomUserSignUpView):

    form_class = TeacherCreationForm


class SchoolAdminSignUpView(CustomUserSignUpView):

    form_class = SchoolAdminCreationForm


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


def verify_email(request, uid64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = CustomUser.objects.get(pk=uid)
    except CustomUser.DoesNotExist:
        user = None
    if request.method == "POST":

        if not user.email_verified:
            send_activation_email(user, request)
            return HttpResponse('New verification has been sent')
        return HttpResponse("Already Verified", status=418)
    if user and generate_token.check_token(user, token):
        user.email_verified = True
        user.save()
        return redirect(reverse('login'))
    return render(request, "registration/invalid_verification_token.html")
