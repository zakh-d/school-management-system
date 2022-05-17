import json

from django.test import TestCase

from accounts.models import CustomUser
from apiv1.serializers import UserSerializer
from school.models import School, Class


class UserSerializerTests(TestCase):

    def setUp(self):
        school = School.objects.create(name='test school')
        user = CustomUser(
            first_name='TEST',
            last_name='TEST',
            username='test',
            email='test@mail.com',
            school=school,
            role=CustomUser.Roles.ADMIN_MEMBER
        )
        user.set_password('testpass123')
        user.save()
        self.serializer = UserSerializer(user)

    def test_school_serializes_to_name(self):
        self.assertEqual(self.serializer.data['school'], 'test school')

    def test_role_serializer_to_string(self):
        self.assertEqual(self.serializer.data['role'], 'Administration Member')


class AvailableClassesAPIViewTests(TestCase):

    def setUp(self):
        self.school = School.objects.create(name='test school')
        self.user = CustomUser(
            first_name='TEST',
            last_name='TEST',
            username='test',
            email='test@mail.com',
            role=CustomUser.Roles.ADMIN_MEMBER
        )
        self.user.set_password('testpass123')
        self.user.save()
        for i in range(3):
            Class.objects.create(name=f'{i+1}-A', school=self.school)

    def test_unauthorized_user_403(self):
        response = self.client.get('/api/v1/classes/')
        self.assertEqual(response.status_code, 403)

    def test_user_without_school_403(self):
        self.client.login(username='test', password='testpass123')
        response = self.client.get('/api/v1/classes/')
        self.assertEqual(response.status_code, 403)

    def test_user_with_school(self):
        self.user.school = self.school
        self.user.save()
        self.client.login(username='test', password='testpass123')
        response = self.client.get('/api/v1/classes/')
        self.assertEqual(response.status_code, 200)

    def test_teacher_gets_only_his_classes(self):
        self.user.school = self.school
        self.user.role = CustomUser.Roles.TEACHER
        self.user.save()

        self.client.login(username='test', password='testpass123')
        response = self.client.get('/api/v1/classes/')
        self.assertEqual(json.loads(response.content), [])


class StudentsFromClassAPIViewTests(TestCase):

    def setUp(self):
        self.user = CustomUser(
            username='test',
            email='test@mail.com',
            role=CustomUser.Roles.ADMIN_MEMBER
        )
        self.user.set_password('testpass123')
        self.user.save()
        self.school = School.objects.create(name='test school')
        self.cls = Class.objects.create(name='1-A', school=self.school)

    def test_admin_not_belong_to_school_403(self):
        self.client.login(username='test', password='testpass123')
        response = self.client.get('/api/v1/classes/' + str(self.cls.id) + '/students/')
        self.assertEqual(response.status_code, 403)

    def test_admin_belong_to_school_200(self):
        self.user.school = self.school
        self.user.save()
        self.client.login(username='test', password='testpass123')
        response = self.client.get('/api/v1/classes/' + str(self.cls.id) + '/students/')
        self.assertEqual(response.status_code, 200)

    def test_teacher_not_belongs_to_class_403(self):
        self.user.school = self.school
        self.user.role = CustomUser.Roles.TEACHER
        self.user.save()
        self.client.login(username='test', password='testpass123')
        response = self.client.get('/api/v1/classes/' + str(self.cls.id) + '/students/')
        self.assertEqual(response.status_code, 403)

    def test_teacher_belongs_to_class_200(self):
        self.user.school = self.school
        self.user.role = CustomUser.Roles.TEACHER
        self.user.save()
        self.cls.add_teachers(self.user)
        self.client.login(username='test', password='testpass123')
        response = self.client.get('/api/v1/classes/' + str(self.cls.id) + '/students/')
        self.assertEqual(response.status_code, 200)


class MyInfoAPIViewTests(TestCase):

    def setUp(self):
        self.school = School.objects.create(name='TEST')
        self.user = CustomUser(
            first_name="f_name",
            last_name="l_name",
            username='test',
            email='test@mail.com',
            role=CustomUser.Roles.ADMIN_MEMBER,
            school=self.school
        )
        self.user.set_password('testpass123')
        self.user.save()

    def test_my_info_data(self):
        self.client.login(username='test', password='testpass123')
        response = self.client.get('/api/v1/auth/me/')
        expected_info = {
            'first_name': 'f_name',
            'last_name': 'l_name',
            'role': 'Administration Member',
            'school': 'TEST'
        }
        self.assertDictEqual(json.loads(response.content), expected_info)


class SchoolUpdateAPIView(TestCase):

    def setUp(self):
        self.school = School.objects.create(name='TEST')
        self.user = CustomUser(
            first_name="f_name",
            last_name="l_name",
            username='test',
            email='test@mail.com',
            role=CustomUser.Roles.TEACHER,
            school=self.school
        )
        self.user.set_password('testpass123')
        self.user.save()

    def test_teacher_has_not_access(self):
        self.client.login(username='test', password='testpass123')
        response = self.client.put('/api/v1/school/', data={'name': 'new name'})
        self.assertEqual(response.status_code, 403)

    def test_admin_has_access(self):
        self.user.role = CustomUser.Roles.ADMIN_MEMBER
        self.user.save()
        self.client.login(username='test', password='testpass123')
        response = self.client.put('/api/v1/school/', data={'name': 'new name'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.school.refresh_from_db()
        self.assertEqual(self.school.name, 'new name')
