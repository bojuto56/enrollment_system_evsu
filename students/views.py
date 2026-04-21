from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Student
from .forms import StudentRegistrationForm, StudentProfileForm


def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            student = Student.objects.create(
                user=user,
                student_id=form.cleaned_data['student_id'],
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                course=form.cleaned_data['course'],
                year_level=form.cleaned_data['year_level']
            )

            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('course_list')
    else:
        form = StudentRegistrationForm()

    return render(request, 'students/register.html', {'form': form})


@login_required
def profile(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'students/profile.html', {'student': student})


@login_required
def edit_profile(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'students/edit_profile.html', {'form': form})