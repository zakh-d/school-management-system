from django.contrib.auth.models import AbstractUser
from django.db import models


USER_ROLES = (
    (0, "Teacher"),
    (1, "Admin"),
)


class CustomUser(AbstractUser):

    role = models.IntegerField(choices=USER_ROLES)

