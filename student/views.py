from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
import pandas as pd

from accounts.models import CustomUser
from school.models import Class
from student.forms import StudentExcelUploadForm
from student.models import Student


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
        file = form.cleaned_data['file']
        df = pd.read_excel(file.temporary_file_path())
        students_dict = df.to_dict()
        origin_class = self.get_object()
        for i in range(len(df)):
            order_in_class = students_dict['order_in_class'].get(i)
            first_name = students_dict['first_name'].get(i)
            last_name = students_dict['last_name'].get(i)
            email = students_dict['email'].get(i)
            email = email if email != 'nan' else None
            phone_number = students_dict['phone_number'].get(i)
            phone_number = phone_number if phone_number != 'nan' else None
            Student.objects.create(
                order_in_class=order_in_class,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                origin_class=origin_class
            )

        return super(UploadStudentsExcelView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UploadStudentsExcelView, self).get_context_data(**kwargs)
        context['class'] = self.get_object()
        return context

    def get_success_url(self):
        return self.get_object().get_absolute_url()
