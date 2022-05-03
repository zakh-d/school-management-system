from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from accounts.models import AdministrationMember
from school.models import Class, School


class ClassDetailPageTests(TestCase):

    def setUp(self):
        admin = AdministrationMember(
            first_name="test",
            last_name="test",
            username="test",
            email="test@mail.com",
        )
        admin.set_password('testpass123')
        admin.save()
        school = School.objects.create(name="test school")
        self._class = Class.objects.create(name="5-A", school=school)

    def test_add_teacher_get_method_405(self):
        url = reverse('school:add_teacher', kwargs={'id': self._class.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_add_teacher_raise_404(self):
        url = reverse('school:add_teacher', kwargs={'id': '123e4567-e89b-12d3-a456-426614174000'})  # random uuid
        self.client.login(username="test", password="testpass123")
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
