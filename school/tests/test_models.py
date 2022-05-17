from django.test import TestCase
from school.models import School, Class


class SchoolModelTest(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='TEST SCHOOL')

    def test_str_method(self):
        self.assertEqual(self.school.__str__(), self.school.name)

    def test_get_by_id(self):
        self.assertEqual(self.school, School.get_by_id(self.school.id))
        self.assertIsNone(School.get_by_id('e05a4115-4341-43a4-9524-1ecfbf980241'))


class ClassModelTest(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='TEST SCHOOL')
        self.test_class = Class.objects.create(name='10-A', school=self.school)

    def test_str_method(self):
        self.assertEqual(self.test_class.__str__(), self.test_class.name)

    def test_get_by_id(self):
        self.assertEqual(self.test_class, Class.get_by_id(self.test_class.id))
        self.assertIsNone(Class.get_by_id('e05a4115-4341-43a4-9524-1ecfbf980241'))

    def test_increase_class_number(self):
        self.test_class.increase_class_number()
        self.test_class.refresh_from_db
        self.assertEqual(self.test_class.name, '11-A')

    def test_order_by_name(self):
        self.school_B = School.objects.create(name='TEST SCHOOL B')
        self.class9B = Class.objects.create(name='9-B', school=self.school_B)
        self.class10B = Class.objects.create(name='10-B', school=self.school_B)
        self.class11B = Class.objects.create(name='11-B', school=self.school_B)

        self.assertListEqual(
            list(Class.order_by_name(self.school_B.classes.all(), True)),
            [self.class11B, self.class10B, self.class9B]
        )
        self.assertListEqual(
            list(Class.order_by_name(self.school_B.classes.all(), False)),
            [self.class9B, self.class10B, self.class11B]
        )
