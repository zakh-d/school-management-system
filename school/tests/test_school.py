from django.test import TestCase, Client
from django.urls import reverse, resolve

from school.models import School
from school.views import CreateSchoolView


class SchoolCreateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.create_url = reverse('school:create_school')
        self.response = self.client.get(self.create_url)

    def test_school_create_view_get(self):
        view = resolve(self.create_url).func.view_class
        self.assertEqual(view, CreateSchoolView)
        self.assertEqual(self.response.status_code, 200)

    def test_school_create_template(self):
        self.assertTemplateUsed(self.response, 'school/create_school.html')


class UpdateSchoolView(TestCase):

    def setUp(self):
        self.client = Client()
        self.school = School.objects.create(name='TEST SCHOOL')
        self.update_url = reverse('school:update_school', kwargs={'pk': self.school.id})
        self.response = self.client.get(self.update_url)

    def test_school_update_view(self):
        view = resolve(self.update_url).func.view_class
        self.assertEqual(view.__name__, UpdateSchoolView.__name__)
        self.assertEqual(self.response.status_code, 200)

    def test_school_update_template(self):
        self.assertTemplateUsed(self.response, 'school/create_school.html')
