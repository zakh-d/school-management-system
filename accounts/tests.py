from django.conf.global_settings import LOGIN_REDIRECT_URL, LOGIN_URL
from django.core import mail
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse, resolve
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.backends import CustomUserModelBackend
from accounts.forms import SchoolAdminCreationForm, TeacherCreationForm, LoginForm
from accounts.models import Teacher, AdministrationMember, CustomUser
from accounts.utils import generate_token, send_activation_email
from accounts.views import SchoolAdminSignUpView, TeacherSignUpView, login_view
from school.models import School


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
            first_name='John',
            last_name='Adams'
        )
        self.assertEqual(str(user), 'John Adams')


class TeacherTests(TestCase):

    def setUp(self):
        self.teacher = Teacher(
            username='test',
            email='test@mail.com',
            password='testpass123',
            first_name='Name',
            last_name='Surname'
        )
        self.teacher.save()
        AdministrationMember.objects.create(
            username='test1',
            email='test1@mail.com',
            password='testpass123',
            first_name='Name',
            last_name='Surname'
        )
        self.school = School.objects.create(name='Test School')

    def test_teacher_save(self):
        self.assertEqual(self.teacher.role, CustomUser.Roles.TEACHER)

    def test_teacher_queryset(self):
        results_count = Teacher.objects.all().count()
        self.assertEqual(results_count, 1)

    def test_teacher_creation_form(self):
        form = TeacherCreationForm(data={
            'first_name': 'Test',
            'last_name': 'Test',
            'username': 'test2',
            'email': 'test2@mail.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'school_id': self.school.id
        })
        self.assertEqual(len(form.errors), 0)
        teacher = form.save()
        self.assertEqual(teacher.school, self.school)

    def test_teacher_creation_form_invalid_school_id(self):
        form = TeacherCreationForm(data={
            'first_name': 'Test',
            'last_name': 'Test',
            'username': 'test2',
            'email': 'test2@mail.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'school_id': '550e8400-e29b-41d4-a716-446655440000'
        })
        self.assertEqual(form.errors['school_id'], ['School with given id does not exist'])


class AdministrationMemberTests(TestCase):

    def setUp(self) -> None:
        self.school_admin = AdministrationMember(
            username='test',
            email='test@mail.com',
            password='testpass123',
            first_name='Name',
            last_name='Surname'
        )
        self.school_admin.save()
        Teacher.objects.create(
            username='test1',
            email='test1@mail.com',
            password='testpass123',
            first_name='Name',
            last_name='Surname'
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

    def test_email_sent_after_signup(self):
        url = reverse('sign_up_admin')
        response = self.client.post(url, data={
            'first_name': 'Test',
            'last_name': 'Test',
            'username': 'test2',
            'email': 'test2@mail.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertEqual(len(mail.outbox), 1)


class LoginPageTests(TestCase):

    def setUp(self):
        url = reverse('login')
        self.response = self.client.get(url)
        user = CustomUser(
            username="test",
            email="mail@mail.com",
        )
        user.set_password('testpass123')
        user.save()

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

    def test_login_success(self):
        url = reverse('login')
        response = self.client.post(url, data={
            'username_or_email': 'test',
            'password': 'testpass123'
        })
        self.assertRedirects(response, LOGIN_REDIRECT_URL)

    def test_login_failed(self):
        url = reverse('login')
        response = self.client.post(url, data={
            'username_or_email': 'test',
            'password': 'incorrect'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('registration/login.html')
        self.assertTrue(response.context.get('error'))
        self.assertContains(response, 'Incorrect credentials were provided')


class TokenGeneratorTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='test',
            email='test@mail.com',
            password='testpass123'
        )
        self.token = generate_token.make_token(self.user)

    def test_token_valid(self):
        self.assertTrue(generate_token.check_token(self.user, self.token))


class EmailVerificationTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='test',
            email='test@mail.com',
            password='testpass123'
        )

    def test_email_sent(self):
        factory = RequestFactory()
        request = factory.get('/')
        send_activation_email(self.user, request)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Verify Email')

    def test_email_verification_template(self):
        token = generate_token.make_token(self.user)
        url = reverse('verify', kwargs={'uid64': urlsafe_base64_encode(force_bytes(self.user.pk)), 'token': token})
        response = self.client.get(url)
        self.assertRedirects(response, LOGIN_URL)
        self.user.refresh_from_db()
        self.assertTrue(self.user.email_verified)

    def test_incorrect_token(self):
        url = reverse('verify', kwargs={'uid64': urlsafe_base64_encode(force_bytes(4)), 'token': "incorrect-token"})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'registration/invalid_verification_token.html')

    def test_resent_verification(self):
        token = generate_token.make_token(self.user)
        url = reverse('verify', kwargs={'uid64': urlsafe_base64_encode(force_bytes(self.user.pk)), 'token': token})
        response = self.client.post(url)
        self.assertContains(response, 'New verification has been sent')

    def test_resent_verification_already_verified(self):
        token = generate_token.make_token(self.user)
        self.user.email_verified = True
        self.user.save()
        url = reverse('verify', kwargs={'uid64': urlsafe_base64_encode(force_bytes(self.user.pk)), 'token': token})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 418)


class CustomUserBackendTests(TestCase):

    def setUp(self):
        self.user = CustomUser(
            username="test",
            email="test@mail.com",
            email_verified=True
        )
        self.user.set_password('testpass123')
        self.user.save()
        self.authenticate = CustomUserModelBackend().authenticate

    def test_custom_authenticate_with_username(self):
        request = RequestFactory().get(reverse('login'))
        user = self.authenticate(request, username="test", password='testpass123')
        self.assertEqual(user.pk, self.user.pk)

    def test_custom_authenticate_with_email(self):
        request = RequestFactory().get(reverse('login'))
        user = self.authenticate(request, username="test@mail.com", password='testpass123')
        self.assertEqual(user.pk, self.user.pk)

