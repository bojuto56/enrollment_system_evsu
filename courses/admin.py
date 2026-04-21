from django.contrib import admin
from django import forms
from .models import Course, Enrollment, Schedule


class ScheduleAdminForm(forms.ModelForm):
    start_time = forms.TimeField(
        input_formats=['%I:%M %p'],
        widget=forms.TimeInput(format='%I:%M %p', attrs={'placeholder': '08:00 AM'})
    )
    end_time = forms.TimeField(
        input_formats=['%I:%M %p'],
        widget=forms.TimeInput(format='%I:%M %p', attrs={'placeholder': '10:00 AM'})
    )

    class Meta:
        model = Schedule
        fields = '__all__'


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleAdminForm
    list_display = ('course', 'day', 'start_time', 'end_time', 'room')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')