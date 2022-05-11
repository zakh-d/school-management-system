import re
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

    @staticmethod
    def get_by_id(id):
        try:
            return School.objects.get(id=id)
        except School.DoesNotExist:
            return None


class Class(models.Model):

    id = models.UUIDField(
         primary_key=True,
         default=uuid.uuid4,
         editable=False)
    name = models.CharField(max_length=4)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    teachers = models.ManyToManyField("accounts.CustomUser", related_name="classes", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("school", "name")

    def add_teachers(self, *teachers):
        self.teachers.add(*teachers)
        self.save()

    def increase_class_number(self):
        """
            Be careful so that wasn't IntegrityError.
            For this when updating class for example 3-A there mustn't be 4-A in same school.
            If using in loop, order_by name desc
        """
        pattern = r"[0-9]+"
        grade = int(re.search(pattern, self.name).group(0))
        self.name = re.sub(pattern, str(grade + 1), self.name)
        self.save()

    def get_absolute_url(self):

        return reverse('school:class_detail', kwargs={"pk": self.id})

    @staticmethod
    def get_by_id(id):
        try:
            return Class.objects.get(id=id)
        except Class.DoesNotExist:
            return None
