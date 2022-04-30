from django.contrib.auth.decorators import user_passes_test

from accounts.models import CustomUser


def admin_required(login_url=None):
    return user_passes_test(lambda user: user.role == CustomUser.Roles.ADMIN_MEMBER, login_url)
