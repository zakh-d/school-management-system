from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView

from accounts.models import CustomUser
from school.forms import CreateUpdateClassForm, AddTeacherClassForm
from school.models import Class
from school.models import School
from school.permissions import admin_required


# School Views


class CreateSchoolView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = School
    fields = ['name']
    template_name = 'school/create_school.html'
    success_url = reverse_lazy('school:dashboard')
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
    template_name = 'school/update_school.html'
    success_url = reverse_lazy('school:dashboard')
    login_url = reverse_lazy('login')

    def has_permission(self):
        return self.request.user.school == self.get_object() \
               and self.request.user.role == CustomUser.Roles.ADMIN_MEMBER


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'school/dashboard.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['is_admin'] = self.request.user.role == CustomUser.Roles.ADMIN_MEMBER
        if self.request.user.school is None:
            context['school'] = None
            return context

        context['school'] = self.request.user.school
        if self.request.user.role == CustomUser.Roles.ADMIN_MEMBER:
            context['classes'] = Class.order_by_name(self.request.user.school.classes.all())
        if self.request.user.role == CustomUser.Roles.TEACHER:
            context['classes'] = Class.order_by_name(self.request.user.classes.all())
        return context


class DashboardReactView(TemplateView):

    template_name = 'index.html'


# Class View

class ClassCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Class
    login_url = reverse_lazy('login')
    template_name = "class/create.html"
    form_class = CreateUpdateClassForm

    def has_permission(self):
        """Checking whether user belongs to any school. No matter user is teacher or admin"""
        return self.request.user.school is not None

    def get_form_kwargs(self):
        kwargs = super(ClassCreateView, self).get_form_kwargs()
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        """Adding school to newly created class and adding teacher if teacher creates class"""
        new_class = form.save(commit=False)
        new_class.school = self.request.user.school
        new_class.save()
        messages.success(self.request, f'New class {new_class.name} successfully created')
        if self.request.user.role == CustomUser.Roles.TEACHER:
            new_class.add_teachers(self.request.user)
        return super(ClassCreateView, self).form_valid(form)


class ClassDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = Class
    login_url = reverse_lazy('login')
    template_name = 'class/detail.html'
    context_object_name = "class"

    def has_permission(self):
        """Can access if user in Class.teachers or it is admin and Class.school==user.school"""
        if self.request.user in self.get_object().teachers.all():
            return True
        if self.request.user.role == CustomUser.Roles.ADMIN_MEMBER and \
                self.get_object().school == self.request.user.school:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ClassDetailView, self).get_context_data(**kwargs)
        context['is_admin'] = self.request.user.role == CustomUser.Roles.ADMIN_MEMBER
        context['add_teacher_form'] = AddTeacherClassForm(school=self.get_object().school, instance=self.get_object())
        context['students'] = self.object.students.all()
        return context


@require_http_methods(['POST'])
@admin_required(login_url=reverse_lazy('login'))
def class_add_teacher_handler(request, id):
    _class = Class.get_by_id(id)
    if not _class:
        raise Http404()
    form = AddTeacherClassForm(_class.school, request.POST, instance=_class)
    if form.is_valid():
        form.save()
    return redirect(reverse('school:class_detail', kwargs={'pk': id}))


@require_http_methods(['POST'])
@admin_required(login_url=reverse_lazy('login'))
def increase_classes_number_handler(request, school_id):
    school = School.get_by_id(school_id)
    if not school:
        raise Http404()
    # TODO: change sorting
    # the -name working not correct with 9 and 10 for example
    classes = Class.order_by_name(school.classes.all(), True)
    for _class in classes:
        _class.increase_class_number()
    messages.success(request, 'All classes\' names updated')
    return redirect(reverse('school:dashboard'))
