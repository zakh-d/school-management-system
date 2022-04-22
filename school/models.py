import uuid
from django.db import models


class School(models.Model):
    id = models.UUIDField(
         primary_key=True,
         default=uuid.uuid4,
         editable=False)
    name = models.CharField(max_length=255)


class Class(models.Model):
    id = models.UUIDField(
         primary_key=True,
         default=uuid.uuid4,
         editable=False)
    name = models.CharField(max_length=4)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    teachers = models.ManyToManyField("Teacher", related_name="classes")

    class Meta:
        unique_together = ("school", "name")

    def add_teachers(self, *teachers):
        self.teachers.add(*teachers)
        self.save()
