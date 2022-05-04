from django.http import Http404
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from accounts.models import AdministrationMember, Teacher
from school.models import Class, School
from school.forms import AddTeacherClassForm


class ClassDetailPageTests(TestCase):

    def setUp(self):
        admin = AdministrationMember(
            first_name='test',
            last_name='test',
            username='test',
            email='test@mail.com',
        )
        admin.set_password('testpass123')
        admin.save()
        self.school = School.objects.create(name='test school')
        self._class = Class.objects.create(name='5-A', school=self.school)
        self.client.login(username='test', password='testpass123')

    def test_add_teacher_get_method_405(self):
        url = reverse('school:add_teacher', kwargs={'id': self._class.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_add_teacher_raise_404(self):
        url = reverse('school:add_teacher', kwargs={'id': '123e4567-e89b-12d3-a456-426614174000'})  # random uuid
        self.client.post(url)
        self.assertRaises(Http404)

    def test_add_teacher(self):
        url = reverse('school:add_teacher', kwargs={'id': self._class.id})
        teacher = Teacher.objects.create(
            first_name='test1',
            last_name='test1',
            username='test1',
            email='test1@mail.com',
            password='testpass123',
            school=self.school
        )
        add_teacher_form = AddTeacherClassForm(data={'teachers': [str(teacher.id)]})
        response = self.client.post(url, data=add_teacher_form.data)
        self._class.refresh_from_db()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(self._class.teachers.count(), 1)


class IncreaseClassNameTests(TestCase):

    def setUp(self):
        self.school = School.objects.create(name='Test School')
        self.class1 = Class.objects.create(name='1-A', school=self.school)
        self.class2 = Class.objects.create(name='6-B', school=self.school)
        admin = AdministrationMember(
            username='test',
            email='test@mail.com'
        )
        admin.set_password('testpass123')
        admin.save()
        self.client.login(username="test", password="testpass123")

    def test_get_method_rejected(self):
        url = reverse('school:increase_class', kwargs={'school_id': self.school.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_raise_404(self):
        url = reverse('school:increase_class', kwargs={'school_id': '123e4567-e89b-12d3-a456-426614174000'})
        self.client.post(url)
        self.assertRaises(Http404)

    def test_class_name_increases(self):
        url = reverse('school:increase_class', kwargs={'school_id': self.school.id})
        self.client.post(url)
        self.class1.refresh_from_db()
        self.class2.refresh_from_db()

        self.assertEqual(self.class1.name, '2-A')
        self.assertEqual(self.class2.name, '7-B')
