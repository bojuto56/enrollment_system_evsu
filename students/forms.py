from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    student_id = forms.CharField(max_length=20)
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    course = forms.CharField(max_length=100, required=False)
    year_level = forms.IntegerField(required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        if Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("Student ID already exists.")
        return student_id

    def clean_email(self):
        email = self.cleaned_data['email']
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'email', 'course', 'year_level']