from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import AdministrationMember
from school.forms import CreateSchoolForm
from school.models import School
from school.views import CreateSchoolView


class SchoolCreateViewTest(TestCase):

    def setUp(self):
        self.school = School.objects.create(name='TEST SCHOOL')
        admin1 = AdministrationMember.objects.create(username='testuser1')
        admin1.set_password('testpass123')
        admin1.save()
        admin2 = AdministrationMember.objects.create(username='testuser2', school=self.school)
        admin2.set_password('testpass456')
        admin2.save()
        self.url = reverse('school:create_school')


    def test_school_create_view_get(self):
        self.client.login(username='testuser1', password='testpass123')
        view = resolve(self.url).func.view_class

        self.assertEqual(view, CreateSchoolView)

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

        self.assertEqual(response.status_code, 403)


    def test_school_create_form(self):
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.post(self.url, data={'name': self.school.name})

        self.assertEqual(response.status_code, 403)

    def test_school_create_form_unittest_base(self):
        """
        One more variant of test_school_create_form
        """
        self.client.login(username='testuser1', password='testpass123')
        form = CreateSchoolForm(data={'name': self.school.name})

        assert form.is_valid() is False, 'School already exit'


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
