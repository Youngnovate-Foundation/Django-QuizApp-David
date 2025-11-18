from django.shortcuts import render

from .models import Quiz, Question, Answer

# Create your views here.
def stu_home(request):
    return render(request, 'quiz_app/Student/stu_home.html')

def inst_home(request):
    return render(request, 'quiz_app/Instructor/inst_home.html')