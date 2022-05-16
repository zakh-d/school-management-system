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
        self.client.login(usename='test', password='testpass123')
        response = self.client.get('/api/v1/classes/')
        self.assertEqual(response.status_code, 200)
