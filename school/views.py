from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from school.models import Class
from school.forms import CreateSchoolForm
from school.models import School


class ClassCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Class
    login_url = reverse_lazy('login')
    fields = ('name',)

    def has_permission(self):
        """Checking whether user belongs to any school. No matter user is teacher or admin"""
        return self.request.user.school is not None

    def form_valid(self, form):

        form.instance.school = self.request.user.school
        super(ClassCreateView, self).form_valid(form)


def school_list(request):
    return render(request, 'school_list.html', {'list': School.objects.all()})


def school_create(request):

    form = CreateSchoolForm

    if request.method == 'POST':
        form = CreateSchoolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'school_create.html', context)


def school_update(request, pk):

    school = School.objects.get(id=pk)
    form = CreateSchoolForm(instance=school)

    if request.method == 'POST':
        form = CreateSchoolForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            return redirect('school-list')

    context = {'form': form}
    return render(request, 'school_update.html', context)


def school_delete(request, pk):

    school = School.objects.get(id=pk)

    if request.method == "POST":
        school.delete()
        return redirect('school-list')

    return render(request, 'school_delete.html', {'item': school})
