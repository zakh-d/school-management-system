from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from accounts.models import CustomUser
from school.forms import CreateUpdateClassForm
from school.models import Class
from school.models import School


# School Views

class CreateSchoolView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = School
    fields = ['name']
    template_name = 'school/create.html'
    success_url = reverse_lazy('profile')
    login_url = reverse_lazy('login')

    def has_permission(self):
        user = self.request.user
        return user.role == CustomUser.Roles.ADMIN_MEMBER and user.school is None

    def form_valid(self, form):
        response = super(CreateSchoolView, self).form_valid(form)
        self.request.user.school = self.object
        self.request.user.save()
        return response


class UpdateSchoolView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = School
    fields = ['name']
    template_name = 'school/update.html'
    success_url = reverse_lazy('school-list')
    login_url = reverse_lazy('login')

    def has_permission(self):
        return self.request.user.school == self.get_object() and self.request.user.role == CustomUser.Roles.ADMIN_MEMBER


# Class View

class ClassCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Class
    login_url = reverse_lazy('login')
    template_name = "class/create.html"

    def has_permission(self):
        """Checking whether user belongs to any school. No matter user is teacher or admin"""
        return self.request.user.school is not None

    def get_form(self, *args, **kwargs):
        return CreateUpdateClassForm(self.request.user, *args, **kwargs)


class ClassDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = Class
    login_url = reverse_lazy('login')
    template_name = 'class/detail.html'
    context_object_name = "class"

    def has_permission(self):
        return self.get_object().school == self.request.user.school
