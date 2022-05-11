from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import CustomUser
from school.models import School, Class
from school.views import DashboardView


class DashboardViewTest(TestCase):

    def setUp(self):
        self.school1 = School.objects.create(name='School1')
        self.school2 = School.objects.create(name='School2')
        self.classA = Class.objects.create(name='1-A', school=self.school1)
        self.classB = Class.objects.create(name='1-B', school=self.school1)
        self.classC = Class.objects.create(name='1-C', school=self.school2)
        self.classD = Class.objects.create(name='1-D', school=self.school2)

        self.admin = CustomUser.objects.create(
            first_name='Admin', last_name='Admin',
            school=self.school1,
            role=1, username='Admin'
        )
        self.admin.set_password('testpass_admin')
        self.admin.save()
        self.teacher = CustomUser.objects.create(
            first_name='Teacher', last_name='Teacher',
            school=self.school2,
            role=0, username='Teacher'
        )
        self.teacher.set_password('testpass_teacher')
        self.teacher.save()

        self.admin_without_school = CustomUser.objects.create(
            first_name='admin_without_school', last_name='admin_without_school',
            school=None,
            role=1, username='admin_without_school'
        )
        self.admin_without_school.set_password('testpass_admin_without_school')
        self.admin_without_school.save()

    def test_dashboard_get_view(self):
        self.client.login(username='Admin', password='testpass_admin')
        view = resolve('/school/dashboard/')

        self.assertEqual(view.func.__name__, DashboardView.as_view().__name__)

    def test_dashboard_admin_get_context_data(self):
        self.client.login(username='Admin', password='testpass_admin')
        response = self.client.get(reverse('school:dashboard'))

        self.assertEqual(response.context['school'], self.school1)

    def test_dashboard_teacher_get_context_data(self):
        self.client.login(username='Teacher', password='testpass_teacher')
        self.classC.teachers.add(self.teacher)
        self.classC.save()
        self.classD.teachers.add(self.teacher)
        self.classD.save()
        response = self.client.get(reverse('school:dashboard'))
        classes = self.teacher.classes.all()

        self.assertQuerysetEqual(response.context['classes'], classes, ordered=False)

    def test_dashboard_get_context(self):
        self.client.login(username='admin_without_school', password='testpass_admin_without_school')
        response = self.client.get(reverse('school:dashboard'))

        self.assertEqual(response.context['school'], None)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/dashboard.html')
