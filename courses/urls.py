from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),
    path('my-enrollments/', views.my_enrollments, name='my_enrollments'),
    path('my-schedule/', views.my_schedule, name='my_schedule'),
]
