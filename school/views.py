from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from accounts.models import CustomUser
from school.forms import CreateUpdateClassForm, AddTeacherClassForm
from school.models import Class
from school.models import School


# School Views
from school.permissions import admin_required


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
            context['classes'] = self.request.user.school.classes.all()
        if self.request.user.role == CustomUser.Roles.TEACHER:
            context['classes'] = self.request.user.classes.all()
        return context


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
        if self.request.user.role == CustomUser.Roles.TEACHER:
            print(type(self.request.user))
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
        return context


@admin_required(login_url=reverse_lazy('login'))
def class_add_teacher_handler(request, id):
    """Handles only POST method"""
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    _class = Class.objects.get(id=id)
    form = AddTeacherClassForm(_class.school, request.POST, instance=_class)
    if form.is_valid():
        form.save()
    return redirect(reverse('school:class_detail', kwargs={'pk': id}))

