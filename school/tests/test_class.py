from http import HTTPStatus

from django.http import Http404
from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser, Teacher, AdministrationMember
from school.forms import AddTeacherClassForm
from school.models import School, Class


class ClassCreateViewTest(TestCase):

    def setUp(self):
        self.school = School.objects.create(name='TEST SCHOOL')
        self.teacher = CustomUser.objects.create(
            first_name='test_user', last_name='test_user',
            username='test_user', school=self.school
        )
        self.teacher.set_password('test_pass')
        self.teacher.save()

    def test_class_create_has_permission(self):
        self.client.login(username='test_user', password='test_pass')
        response = self.client.get(reverse('school:class_create'))

        self.assertEqual(response.status_code, 200)

    def test_form_kwargs(self):
        self.client.login(username='test_user', password='test_pass')

        response = self.client.get(reverse('school:class_create'))

        self.assertEqual(response.context.get('form').school, self.school)

    def test_form_valid(self):
        self.client.login(username='test_user', password='test_pass')
        self.client.post(reverse('school:class_create'), data={'name': '11-A'})

        _class = Class.objects.last()
        self.assertEqual(_class.school, self.school)
        self.assertTrue(self.teacher in _class.teachers.all())

    def test_redirects_after_POST_request(self):
        self.client.login(username='test_user', password='test_pass')
        response = self.client.post(reverse('school:class_create'), data={'name': '11-A'})
        _class = Class.objects.last()
        self.assertRedirects(response, _class.get_absolute_url())


class ClassDetailViewTest(TestCase):

    def setUp(self):
        self.school = School.objects.create(name='TEST SCHOOL')
        self.fake_school = School.objects.create(name='FAKE TEST SCHOOL')
        self.test_class = Class.objects.create(name='11-A', school=self.school)
        self.admin = CustomUser.objects.create(
            first_name='Admin', last_name='Admin',
            school=self.school,
            role=1, username='Admin'
        )
        self.admin.set_password('testpass_admin')
        self.admin.save()
        self.teacher = CustomUser.objects.create(
            first_name='Teacher', last_name='Teacher',
            school=self.school,
            role=0, username='Teacher'
        )
        self.teacher.set_password('testpass_teacher')
        self.teacher.save()
        self.test_class.teachers.add(self.teacher)
        self.test_class.save()
        self.fake_admin = CustomUser.objects.create(
            first_name='fakeAdmin', last_name='fakeAdmin',
            school=self.fake_school,
            role=1, username='fakeAdmin'
        )
        self.fake_admin.set_password('testpass_fake_admin')
        self.fake_admin.save()

    def test_has_permission_teacher(self):
        self.client.login(username='Teacher', password='testpass_teacher')
        response = self.client.get(reverse('school:class_detail', kwargs={'pk': self.test_class.id}))

        self.assertIn(response.context['user'], self.test_class.teachers.all())
        self.assertNotEqual(response.context['user'].role, 1)

    def test_has_permission_admin(self):
        self.client.login(username='Admin', password='testpass_admin')
        response = self.client.get(reverse('school:class_detail', kwargs={'pk': self.test_class.id}))

        self.assertEqual(response.context['user'].role, 1)

    def test_has_no_permission_fake_admin(self):
        self.client.login(username='fakeAdmin', password='testpass_fake_admin')
        response = self.client.get(reverse('school:class_detail', kwargs={'pk': self.test_class.id}))

        self.assertEqual(response.status_code, 403)


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
