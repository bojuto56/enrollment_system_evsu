from django.db import models
from students.models import Student

class Course(models.Model):
    course_code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name


class Schedule(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.course.course_code} - {self.day} ({self.start_time}-{self.end_time})"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"