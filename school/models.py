import uuid
from django.db import models
from django.urls import reverse


class School(models.Model):
    id = models.UUIDField(
         primary_key=True,
         default=uuid.uuid4,
         editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Class(models.Model):

    id = models.UUIDField(
         primary_key=True,
         default=uuid.uuid4,
         editable=False)
    name = models.CharField(max_length=4)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    teachers = models.ManyToManyField("accounts.CustomUser", related_name="classes")

    class Meta:
        unique_together = ("school", "name")

    def add_teachers(self, *teachers):
        self.teachers.add(*teachers)
        self.save()

    def get_absolute_url(self):

        return reverse('class_detail', kwargs={"pk": self.id})
