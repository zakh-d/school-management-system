from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from school.models import Class


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
