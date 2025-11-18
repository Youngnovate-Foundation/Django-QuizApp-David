from django.urls import path
from . import views

urlpatterns = [
    path('student/home/', views.stu_home, name='student_home'),
    path('instructor/home/', views.inst_home, name='instructor_home'),
]