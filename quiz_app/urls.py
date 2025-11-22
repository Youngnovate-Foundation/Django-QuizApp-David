from django.urls import path

from .decourators import instructor_required
from . import views

urlpatterns = [
    path('student/home/', views.stu_home, name='student_home'),
    path('instructor/home/', views.inst_home, name='instructor_home'),
    path('create_quiz/', instructor_required(views.Create_QuizView.as_view()), name='create_quiz'),
    path('add_question/<int:quiz_id>/', instructor_required(views.Add_QuestionView.as_view()), name='add_question'),
    path('view_quiz/<int:quiz_id>/', views.view_qiuz_instructor, name='view_quiz_instructor'),
    #path('take_quiz/<int:quiz_id>/', views.view_quiz_student, name='view_quiz_student'),
]