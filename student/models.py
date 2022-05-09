import uuid
from django.db import models
from school.models import Class


class Student(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    origin_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    photo = models.ImageField(
        upload_to='students_photos/',
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
