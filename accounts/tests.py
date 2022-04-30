from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from accounts.forms import SchoolAdminCreationForm, TeacherCreationForm
from accounts.views import SchoolAdminSignUpView, TeacherSignUpView


class CustomUsersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create(
            username='test_user',
            email='test@mail.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'test@mail.com')
        self.assertEqual(user.role, User.Roles.TEACHER)
        self.assertFalse(user.email_verified)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_super_user(self):
        User = get_user_model()
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@mail.com',
            password='testpass123'
        )
        self.assertEqual(admin.username, 'admin')
        self.assertEqual(admin.email, 'admin@mail.com')
        self.assertFalse(admin.email_verified)
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class SignUpPageTests(TestCase):

    def setUp(self):
        url_admin = reverse('sign_up_admin')
        url_teacher = reverse('sign_up_teacher')
        self.response_admin = self.client.get(url_admin)
        self.response_teacher = self.client.get(url_teacher)

    def test_admin_sign_up_template(self):
        self.assertEqual(self.response_admin.status_code, 200)
        self.assertTemplateUsed(self.response_admin, 'registration/signup.html')
        self.assertNotContains(self.response_admin, 'School ID')

    def test_admin_sign_up_form(self):
        form = self.response_admin.context.get('form')
        self.assertIsInstance(form, SchoolAdminCreationForm)
        self.assertContains(self.response_admin, 'csrfmiddlewaretoken')

    def test_admin_sign_up_view(self):
        view = resolve('/accounts/admin/sign-up/')
        self.assertEqual(
            view.func.__name__,
            SchoolAdminSignUpView.as_view().__name__
        )

    def test_teacher_sign_up_template(self):
        self.assertEqual(self.response_teacher.status_code, 200)
        self.assertTemplateUsed(self.response_teacher, 'registration/signup.html')
        self.assertContains(self.response_teacher, 'School ID')

    def test_teacher_sign_up_form(self):
        form = self.response_teacher.context.get('form')
        self.assertIsInstance(form, TeacherCreationForm)
        self.assertContains(self.response_teacher, 'csrfmiddlewaretoken')

    def test_teacher_sign_up_view(self):
        view = resolve('/accounts/teacher/sign-up/')
        self.assertEqual(
            view.func.__name__,
            TeacherSignUpView.as_view().__name__
        )
