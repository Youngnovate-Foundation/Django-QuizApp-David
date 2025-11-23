from django.urls import path

from .decourators import instructor_required
from . import views

urlpatterns = [
    path('student/home/', views.stu_home, name='student_home'),
    path('instructor/home/', views.inst_home, name='instructor_home'),
    path('instructor/create_quiz/', instructor_required(views.Create_QuizView.as_view()), name='create_quiz'),
    path('instructor/add_question/<int:quiz_id>/', instructor_required(views.Add_QuestionView.as_view()), name='add_question'),
    path('instructor/view_quiz/<int:quiz_id>/', views.view_qiuz_instructor, name='view_quiz_instructor'),
    path('student/quiz_instruction/<int:quiz_id>/', views.quiz_instruction, name='quiz_instruction'),
    path('student/quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('student/quiz/<int:quiz_id>/question/<int:question_id>/', views.quiz_question, name='quiz_question'),
    path('student/quiz/attempt/<int:attempt_id>/finish/', views.quiz_finish, name='quiz_finish'),
    path('student/results/', views.student_results, name='student_results'),
    path('instructor/quiz/<int:quiz_id>/participants/', views.quiz_participants, name='quiz_participants'),
    path('student/quiz/<int:quiz_id>/result/', views.student_quiz_result_detail, name='student_quiz_result_detail'),
]   