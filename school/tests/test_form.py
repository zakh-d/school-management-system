from django.test import TestCase
from school.forms import CreateUpdateClassForm
from school.models import School, Class


class TestCreateUpdateClassForm(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='TEST SCHOOL')
        self.test_class = Class.objects.create(name='11-A', school=self.school)


    def test_clean_name(self):
        form1 = CreateUpdateClassForm(data={'name': '11-A'}, school=self.school)
        form2 = CreateUpdateClassForm(data={'name': '11-B'}, school=self.school)
        form3 = CreateUpdateClassForm(data={'name': '11-C'}, school=None)

        self.assertFalse(form1.is_valid())
        self.assertTrue(form2.is_valid())
        self.assertFalse(form3.is_valid())
