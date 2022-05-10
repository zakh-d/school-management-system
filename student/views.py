from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from accounts.models import CustomUser
from school.models import Class
from student.forms import StudentExcelUploadForm


class UploadStudentsExcelView(LoginRequiredMixin, PermissionRequiredMixin, FormView):

    login_url = reverse_lazy('login')
    template_name = 'student/upload.html'
    form_class = StudentExcelUploadForm

    def get_object(self):
        return get_object_or_404(Class, id=self.kwargs.get('class_id'))

    def has_permission(self):
        class_object = self.get_object()
        user = self.request.user
        if user.role == CustomUser.Roles.ADMIN_MEMBER:
            return user.school == class_object.school
        return user in class_object.teachers.all()

    def form_valid(self, form):
        return super(UploadStudentsExcelView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UploadStudentsExcelView, self).get_context_data(**kwargs)
        context['class'] = self.get_object()
        return context

    def get_success_url(self):
        return self.get_object().get_absolute_url()
