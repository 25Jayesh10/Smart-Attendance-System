from django.urls import path
from . import views

app_name = 'edu'

urlpatterns = [
    path('student/', views.student_dashboard, name = "student_dashboard"),
    path('teacher/', views.teacher_dashboard, name = "teacher_dashboard"),
    path('stu_add/', views.stu_add, name = "stu_add"),
    path('stu_details/', views.stu_details, name = "stu_details"),
    
]
