from django.test import TestCase
from school.forms import CreateUpdateClassForm
from school.models import School, Class


class TestCreateUpdateClassForm(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='TEST SCHOOL')
        self.test_class = Class.objects.create(name='11-A', school=self.school)

    def test_name_validation(self):
        form = CreateUpdateClassForm(data={'name': '9-A'}, school=self.school)

        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_name_validation_not_unique_class(self):
        form = CreateUpdateClassForm(data={'name': '11-A'}, school=self.school)

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertListEqual(form.errors['name'], ['Class 11-A already exists'])

