from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from school.models import School, Class


class TestCreateUpdateClassForm(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='TEST SCHOOL')
        self.test_class = Class.objects.create(name='11-A', school=self.school)
        self.teacher = CustomUser.objects.create(
            first_name='Teacher', last_name='Teacher',
            school=self.school,
            role=0, username='Teacher'
        )
        self.teacher.set_password('testpass_teacher')
        self.teacher.save()

    def test_clean_name(self):
        self.client.login(username='Teacher', password='testpass_teacher')
        response = self.client.post(reverse('school:class_create'), data={'name': self.test_class.name})

        self.assertEqual(response.status_code, 200)