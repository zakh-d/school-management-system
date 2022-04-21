from django.contrib.auth.models import AbstractUser
from django.db import models
from school.models import School


USER_ROLES = (
    (0, "Teacher"),
    (1, "Administration Member"),
)


class CustomUser(AbstractUser):

    email_verified = models.BooleanField(default=False)
    role = models.IntegerField(choices=USER_ROLES, default=0)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True)
