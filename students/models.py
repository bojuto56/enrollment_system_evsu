from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=100, blank=True)
    year_level = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name