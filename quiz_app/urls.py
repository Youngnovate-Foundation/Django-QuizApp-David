from django.urls import path
from . import views

urlpatterns = [
    path('student/home/', views.stu_home, name='student_home'),
    path('instructor/home/', views.inst_home, name='instructor_home'),
    path('create_quiz/', views.Create_QuizView.as_view(), name='create_quiz'),
    path('add_question/<int:quiz_id>/', views.Add_QuestionView.as_view(), name='add_question'),
]