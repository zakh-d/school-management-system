from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from school.models import School, Class


class ClassCreateViewTest(TestCase):

    def setUp(self):
        self.school = School.objects.create(name='TEST SCHOOL')
        self.teacher = CustomUser.objects.create(
            first_name='test_user', last_name='test_user',
            username='test_user'
        )
        self.teacher.set_password('test_pass')
        self.teacher.save()

    def test_class_create_has_permission(self):
        self.teacher.school = self.school
        self.teacher.save()
        self.client.login(username='test_user', password='test_pass')
        response = self.client.get(reverse('school:class_create'))

        self.assertEqual(response.status_code, 200)

    def test_form_kwargs(self):
        self.client.login(username='test_user', password='test_pass')
        self.teacher.school = self.school
        self.teacher.save()

        response = self.client.get(reverse('school:class_create'))

        self.assertEqual(response.context.get('form').school, self.school)

    def test_form_valid(self):
        self.client.login(username='test_user', password='test_pass')
        self.teacher.school = self.school
        self.teacher.save()
        response = self.client.post(reverse('school:class_create'), data={'name': '11-A'})
        response.school = self.school
        response.teacher = self.teacher

        self.assertEqual(response.status_code, 302)


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
