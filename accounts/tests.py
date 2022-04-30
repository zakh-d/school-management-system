from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from accounts.forms import SchoolAdminCreationForm, TeacherCreationForm, LoginForm
from accounts.models import Teacher, AdministrationMember, CustomUser
from accounts.views import SchoolAdminSignUpView, TeacherSignUpView, login_view


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

    def test_custom_user_str(self):
        User = get_user_model()
        user = User.objects.create(
            username='test_user',
            email='test@mail.com',
            password='testpass123',
            first_name="John",
            last_name="Adams"
        )
        self.assertEqual(str(user), "John Adams")


class TeacherTests(TestCase):

    def setUp(self):
        self.teacher = Teacher(
            username="test",
            email="test@mail.com",
            password="testpass123",
            first_name="Name",
            last_name="Surname"
        )
        self.teacher.save()
        AdministrationMember.objects.create(
            username="test1",
            email="test1@mail.com",
            password="testpass123",
            first_name="Name",
            last_name="Surname"
        )

    def test_teacher_save(self):
        self.assertEqual(self.teacher.role, CustomUser.Roles.TEACHER)

    def test_teacher_queryset(self):
        results_count = Teacher.objects.all().count()
        self.assertEqual(results_count, 1)


class AdministrationMemberTests(TestCase):

    def setUp(self) -> None:
        self.school_admin = AdministrationMember(
            username="test",
            email="test@mail.com",
            password="testpass123",
            first_name="Name",
            last_name="Surname"
        )
        self.school_admin.save()
        Teacher.objects.create(
            username="test1",
            email="test1@mail.com",
            password="testpass123",
            first_name="Name",
            last_name="Surname"

        )

    def test_school_admin_save(self):
        self.assertEqual(self.school_admin.role, CustomUser.Roles.ADMIN_MEMBER)

    def test_school_admin_queryset(self):
        results_count = AdministrationMember.objects.all().count()
        self.assertEqual(results_count, 1)


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


class LoginPageTests(TestCase):

    def setUp(self):
        url = reverse('login')
        self.response = self.client.get(url)

    def test_login_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/login.html')
        self.assertContains(self.response, 'Username or email:')

    def test_login_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, LoginForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_login_view(self):
        view = resolve('/accounts/login/')
        self.assertEqual(
            view.func.__name__,
            login_view.__name__
        )
