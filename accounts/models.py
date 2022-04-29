from django.contrib.auth.models import AbstractUser
from django.db import models
from school.models import School


class CustomUser(AbstractUser):

    class Roles(models.IntegerChoices):

        TEACHER = 0, "Teacher"
        ADMIN_MEMBER = 1, "Administration Member"

    email_verified = models.BooleanField(default=False)
    role = models.IntegerField(choices=Roles.choices, default=0)
    school = models.ForeignKey(School, on_delete=models.SET_NULL,
                               null=True,
                               blank=True)


class TeacherManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=CustomUser.Roles.TEACHER)


class AdminMemberManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=CustomUser.Roles.ADMIN_MEMBER)


class Teacher(CustomUser):

    def save(self, *args, **kwargs):
        """Setting teacher role to model on create"""
        if not self.pk:
            self.role = CustomUser.Roles.TEACHER

        super(Teacher, self).save(*args, **kwargs)

    class Meta:
        proxy = True


class AdministrationMember(CustomUser):

    def save(self, *args, **kwargs):
        """Setting admin-member role to model on create"""
        if not self.pk:
            self.role = CustomUser.Roles.ADMIN_MEMBER
        super(AdministrationMember, self).save(*args, **kwargs)

    class Meta:
        proxy = True
