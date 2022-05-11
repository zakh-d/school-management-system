from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import AdministrationMember, CustomUser
from school.models import School, Class
from school.views import CreateSchoolView, DashboardView


class SchoolCreateViewTest(TestCase):

    def setUp(self):
        self.school = School.objects.create(name='TEST SCHOOL')
        self.admin1 = AdministrationMember.objects.create(username='testuser1')
        self.admin1.set_password('testpass123')
        self.admin1.save()
        admin2 = AdministrationMember.objects.create(username='testuser2', school=self.school)
        admin2.set_password('testpass456')
        admin2.save()
        self.url = reverse('school:create_school')


    def test_school_create_view_get(self):
        self.client.login(username='testuser1', password='testpass123')
        view = resolve('/school/create/')

        self.assertEqual(view.func.__name__, CreateSchoolView.as_view().__name__)

    def test_school_create_template(self):
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'school/create_school.html')
        self.assertEqual(response.status_code, 200)

    def test_school_create_template_forbidden_user_has_school(self):
        self.client.login(username='testuser2', password='testpass456', school=self.school)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_school_create_template_forbidden_unregistred_user(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('login') + '?next=' + self.url)


    def test_school_create_view_forbidden_for_user_with_school(self):
        self.client.login(username='testuser2', password='testpass456')
        response = self.client.post(self.url, data={'name': 'TEST SCHOOL'})

        self.assertEqual(response.status_code, 403)

    def test_school_create_form_valid(self):
        self.client.login(username='testuser1', password='testpass123')
        self.client.post(self.url, data={'name': 'TEST SCHOOL'})
        self.admin1.refresh_from_db()

        self.assertIsNotNone(self.admin1.school)


class UpdateSchoolView(TestCase):

    def setUp(self):
        self.school = School.objects.create(name='TEST SCHOOL')
        admin = AdministrationMember.objects.create(username='testuser', school=self.school)
        admin.set_password('testpass123')
        admin.save()
        self.url = reverse('school:update_school', kwargs={'pk': self.school.id})

    def test_school_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        view = resolve(self.url).func.view_class

        self.assertEqual(view.__name__, UpdateSchoolView.__name__)

    def test_school_update_template(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'school/update_school.html')
        self.assertEqual(response.status_code, 200)


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

        self.AdminWithoutSchool = CustomUser.objects.create(
            first_name='AdminWithoutSchool', last_name='AdminWithoutSchool',
            school=None,
            role=1, username='AdminWithoutSchool'
        )
        self.AdminWithoutSchool.set_password('testpass_AdminWithoutSchool')
        self.AdminWithoutSchool.save()

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

    def test_dashboard_get_context_data_forbidden_with_no_school(self):
        self.client.login(username='AdminWithoutSchool', password='testpass_AdminWithoutSchool')
        response = self.client.get(reverse('school:dashboard'))

        self.assertEqual(response.context['school'], None)
        self.assertEqual(response.status_code, 302)