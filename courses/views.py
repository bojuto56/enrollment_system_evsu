from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Course, Enrollment, Schedule
from students.models import Student
from datetime import datetime

def time_overlaps(start1, end1, start2, end2):
    return start1 < end2 and start2 < end1

@login_required
def course_list(request):
    courses = Course.objects.prefetch_related('schedules').all()
    enrolled_course_ids = []

    try:
        student = Student.objects.get(user=request.user)
        enrolled_course_ids = Enrollment.objects.filter(student=student).values_list('course_id', flat=True)
    except Student.DoesNotExist:
        pass

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'enrolled_course_ids': enrolled_course_ids
    })


@login_required
@require_POST
def enroll(request, course_id):
    student = get_object_or_404(Student, user=request.user)
    course = get_object_or_404(Course.objects.prefetch_related('schedules'), id=course_id)

    enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
    if not created:
        messages.warning(request, f"You are already enrolled in {course.course_name}.")
        return redirect('course_list')

    new_schedules = list(course.schedules.all())

    existing_enrollments = Enrollment.objects.filter(student=student).exclude(course=course).select_related('course').prefetch_related('course__schedules')

    for existing in existing_enrollments:
        for existing_sched in existing.course.schedules.all():
            for new_sched in new_schedules:
                same_day = existing_sched.day.strip().lower() == new_sched.day.strip().lower()
                if same_day and time_overlaps(existing_sched.start_time, existing_sched.end_time, new_sched.start_time, new_sched.end_time):
                    enrollment.delete()
                    messages.error(
                        request,
                        f"Schedule conflict: {course.course_name} conflicts with {existing.course.course_name} on {new_sched.day}."
                    )
                    return redirect('course_list')

    messages.success(request, f"You successfully enrolled in {course.course_name}.")
    return redirect('course_list')


@login_required
def my_enrollments(request):
    student = get_object_or_404(Student, user=request.user)
    enrollments = Enrollment.objects.filter(student=student).select_related('course').prefetch_related('course__schedules')

    return render(request, 'courses/my_enrollments.html', {
        'enrollments': enrollments
    })


@login_required
def my_schedule(request):
    student = get_object_or_404(Student, user=request.user)
    enrollments = Enrollment.objects.filter(student=student).select_related('course').prefetch_related('course__schedules')

    schedule_items = []
    for enrollment in enrollments:
        for sched in enrollment.course.schedules.all():
            schedule_items.append({
                'course_code': enrollment.course.course_code,
                'course_name': enrollment.course.course_name,
                'day': sched.day,
                'start_time': sched.start_time,
                'end_time': sched.end_time,
                'room': sched.room,
            })

    day_order = {
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6,
        'sunday': 7,
    }

    schedule_items.sort(
        key=lambda x: (
            day_order.get(x['day'].strip().lower(), 99),
            x['start_time']
        )
    )

    return render(request, 'courses/my_schedule.html', {
        'schedule_items': schedule_items
    })