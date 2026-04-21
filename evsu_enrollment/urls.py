from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('/accounts/login/')

urlpatterns = [
    path('', home_redirect, name='home'),
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('students/', include('students.urls')),  # ✅ ADD THIS LINE
    path('accounts/', include('django.contrib.auth.urls')),
]