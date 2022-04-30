import uuid
from django.db import models
from school.models import Class, School


class Student(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    photo = models.ImageField(
        upload_to=None, max_length=255,
        height_field=None, width_field=None,
        blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    origin_school = models.ForeignKey(School, on_delete=models.CASCADE)
    origin_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
