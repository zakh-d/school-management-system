from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUsersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create(
            username="test_user",
            email="test@mail.com",
            password="testpass123"
        )
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.email, "test@mail.com")
        self.assertEqual(user.role, User.Roles.TEACHER)
        self.assertFalse(user.email_verified)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_super_user(self):
        User = get_user_model()
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@mail.com",
            password="testpass123"
        )
        self.assertEqual(admin.username, "admin")
        self.assertEqual(admin.email, "admin@mail.com")
        self.assertFalse(admin.email_verified)
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
