from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Quiz, Question
from .forms import Quiz_Form, Question_Form
from django.contrib.auth.decorators import login_required
from users.models import CustomUser

# Create your views here.
@login_required
def stu_home(request):
    quizzes = Quiz.objects.all()
    users = CustomUser.objects.all()
    return render(request, 'quiz_app/Student/stu_home.html', {'quizzes': quizzes, 'users': users})

@login_required
def inst_home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_app/Instructor/inst_home.html', {'quizzes': quizzes})

class Create_QuizView(View):
    def get(self, request):
        create_quiz_form = Quiz_Form()
        return render(request, 'quiz_app/Instructor/create_quiz.html', {'create_quiz_form': create_quiz_form})
    
    def post(self, request):
        create_quiz_form = Quiz_Form(request.POST)
        if create_quiz_form.is_valid():
            quiz_instance = create_quiz_form.save(commit=False)
            quiz_instance.user = request.user
            quiz_instance.save()
            messages.success(request, "Quiz created successfully!")
            return redirect('instructor_home')
        else:
            messages.success(request, "Quiz creation Failed")
            return render(request, 'quiz_app/Instructor/create_quiz.html', {'create_quiz_form': create_quiz_form})
        
class Add_QuestionView(View):
    def get(self, request, quiz_id):
        add_question_form = Question_Form()
        return render (request, 'quiz_app/Instructor/add_question.html', {'add_question_form': add_question_form, 'quiz_id': quiz_id})
    
    def post(self, request, quiz_id):
        add_question_form = Question_Form(request.POST)
        if add_question_form.is_valid():
            question = add_question_form.save(commit=False)
            question.quiz_id = quiz_id
            question.save()
            messages.success(request, "Question created successfully!")
            return redirect('instructor_home')
        else:
            messages.error(request, "Question creation Failed")
            return render(request, 'quiz_app/Instructor/add_question.html', {'add_question_form': add_question_form, 'quiz_id': quiz_id})

def view_qiuz_instructor(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'quiz_app/Instructor/view_quiz_instructor.html', {'quiz': quiz,'questions': questions})

def view_quiz_student(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'quiz_app/Student/view_quiz_student.html', {'quiz': quiz,'questions': questions})