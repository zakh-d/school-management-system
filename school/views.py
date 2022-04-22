from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from accounts.models import CustomUser
from school.models import School


class CreateSchoolView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = School
    fields = ['name']
    template_name = 'school/create.html'
    success_url = reverse_lazy('school-list')
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
