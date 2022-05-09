from django.test import TestCase

from school.models import School, Class
from student.models import Student


class StudentModelTests(TestCase):

    def setUp(self):
        school = School.objects.create(name='TEST SCHOOL')
        _class = Class.objects.create(name='10-A', school=school)
        self.student = Student.objects.create(
            first_name='Jack',
            last_name='Sparrow',
            origin_class=_class
        )

    def test_str(self):
        self.assertEqual(str(self.student), 'Jack Sparrow')

