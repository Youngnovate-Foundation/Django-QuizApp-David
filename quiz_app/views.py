from django.utils import timezone
from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from .models import Quiz, Question, Quiz_Attempt, Student_Answer
from .forms import Answer_Form, Quiz_Form, Question_Form
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from .decourators import instructor_required, student_required

# Create your views here.
@login_required
@student_required
def stu_home(request):
    quizzes = Quiz.objects.all()
    users = CustomUser.objects.all()
    return render(request, 'quiz_app/Student/stu_home.html', {'quizzes': quizzes, 'users': users})

@login_required
@instructor_required
def inst_home(request):
    all_quizzes = Quiz.objects.all()
    user_quizzes = all_quizzes.filter(user=request.user)  # Only quizzes created by this instructor
    return render(request, 'quiz_app/Instructor/inst_home.html', {
        'user_quizzes': user_quizzes
    })

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

@instructor_required
def view_qiuz_instructor(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'quiz_app/Instructor/view_quiz_instructor.html', {'quiz': quiz,'questions': questions})

@student_required
def quiz_instruction(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'quiz_app/Student/start_quiz.html', {'quiz': quiz,'questions': questions})

@student_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Check if student already has a COMPLETED attempt
    already_completed = Quiz_Attempt.objects.filter(
        student=request.user,
        quiz=quiz,
        completed_at__isnull=False
    ).exists()

    if already_completed:
        messages.error(request, "You have already completed this quiz. Only one attempt is allowed.")
        return redirect('student_results')  # or redirect('student_home')

    # Check if there's an ongoing (unfinished) attempt
    ongoing_attempt = Quiz_Attempt.objects.filter(
        student=request.user,
        quiz=quiz,
        completed_at__isnull=True
    ).first()

    if ongoing_attempt:
        # Resume the existing attempt
        attempt = ongoing_attempt
    else:
        # Create new attempt (only if no completed one exists)
        attempt = Quiz_Attempt.objects.create(
            student=request.user,
            quiz=quiz,
            time_remaining=quiz.duration * 60
        )

    first_question = quiz.questions.first()
    if not first_question:
        messages.error(request, "This quiz has no questions.")
        return redirect('student_home')

    return redirect('quiz_question', quiz_id=quiz.id, question_id=first_question.id)

@student_required
def quiz_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = get_object_or_404(Question, id=question_id, quiz=quiz)

    attempt = Quiz_Attempt.objects.get(
        student=request.user,
        quiz=quiz,
        completed_at__isnull = True
    )

    # Timer logic
    elapsed = (timezone.now() - attempt.started_at).total_seconds()
    remaining = max(0, (quiz.duration * 60) - elapsed)
    if remaining <= 0:
        return redirect('quiz_finish', attempt_id=attempt.id)
    attempt.time_remaining = int(remaining)
    attempt.save()

    # === Navigation (this is the part that was breaking) ===
    all_questions = list(quiz.questions.all().order_by('id'))  # consistent order
    question_ids = [q.id for q in all_questions]
    
    try:
        current_idx = question_ids.index(question.id)
    except ValueError:
        # question not found (should never happen)
        return redirect('start_quiz', quiz_id=quiz.id)

    prev_question = all_questions[current_idx - 1] if current_idx > 0 else None
    next_question = all_questions[current_idx + 1] if current_idx < len(all_questions) - 1 else None

    saved_answer = Student_Answer.objects.filter(attempt=attempt, question=question).first()

    if request.method == 'POST':
        form = Answer_Form(question, request.POST)
        if form.is_valid():
            # Save answer
            if question.question_type in ['MCQ', 'TF']:
                Student_Answer.objects.update_or_create(
                    attempt=attempt, question=question,
                    defaults={'selected_option': form.cleaned_data.get('selected_option'), 'answer_text': None}
                )
            elif question.question_type == 'SA':
                Student_Answer.objects.update_or_create(
                    attempt=attempt, question=question,
                    defaults={'answer_text': form.cleaned_data.get('answer_text'), 'selected_option': None}
                )

            # Navigation
            if 'next' in request.POST and next_question:
                return redirect('quiz_question', quiz_id=quiz.id, question_id=next_question.id)
            if 'prev' in request.POST and prev_question:
                return redirect('quiz_question', quiz_id=quiz.id, question_id=prev_question.id)
            if 'finish' in request.POST:
                return redirect('quiz_finish', attempt_id=attempt.id)
    else:
        form = Answer_Form(question)
        if saved_answer:
            if question.question_type in ['MCQ', 'TF']:
                form.fields['selected_option'].initial = saved_answer.selected_option
            elif question.question_type == 'SA':
                form.fields['answer_text'].initial = saved_answer.answer_text

    context = {
        'quiz': quiz,
        'question': question,
        'form': form,
        'current': current_idx + 1,
        'total': len(all_questions),
        'prev_q': prev_question,
        'next_q': next_question,
        'time_left': int(remaining),
    }
    return render(request, 'quiz_app/Student/quiz_question.html', context)

# quiz_app/views.py
@student_required
def quiz_finish(request, attempt_id):
    attempt = get_object_or_404(Quiz_Attempt, id=attempt_id, student=request.user)

    # === ALWAYS calculate total_points and earned_points ===
    total_points = 0
    earned_points = 0

    for answer in attempt.student_answer_set.all():
        q = answer.question
        points = q.point or 1
        total_points += points

        if q.question_type == 'MCQ':
            if answer.selected_option == q.correct_option:
                earned_points += points
        elif q.question_type == 'TF':
            if str(answer.selected_option) == q.answer_text_TF:
                earned_points += points
        elif q.question_type == "SA":
                if str(answer.answer_text) == q.answer_text_SA:
                    earned_points += points

    # Save score only if quiz not already finished
    if not attempt.completed_at:
        attempt.score = earned_points
        attempt.completed_at = timezone.now()
        attempt.save()

    # === SAFE CALCULATIONS (NO MORE ERRORS) ===
    earned_points = attempt.score or 0
    total_points = total_points or 1  # prevent division by zero

    if total_points == 0:
        percentage = 0.0
    else:
        percentage = round((earned_points / total_points) * 100, 1)

    context = {
        'attempt': attempt,
        'earned_points': earned_points,
        'total_points': total_points,
        'percentage': percentage,
    }
    return render(request, 'quiz_app/Student/quiz_result.html', context)

@instructor_required
def quiz_participants(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user)  # only own quiz

    # All completed attempts for this quiz
    attempts = Quiz_Attempt.objects.filter(
        quiz=quiz,
        completed_at__isnull=False
    ).select_related('student').order_by('-completed_at')

    # Calculate total points for the quiz once (same for everyone)
    total_points = quiz.questions.aggregate(
        total=models.Sum('point')
    )['total'] or quiz.questions.count()

    for attempt in attempts:
        attempt.total_points = total_points
        attempt.percentage = (
            attempt.score / total_points * 100 if total_points and attempt.score else 0
        )

    context = {
        'quiz': quiz,
        'attempts': attempts,
        'total_points': total_points,
    }
    return render(request, 'quiz_app/Instructor/quiz_participants.html', context)

@student_required
def student_results(request):
    # All completed attempts for this student
    completed_attempts = Quiz_Attempt.objects.filter(
        student=request.user,
        completed_at__isnull=False
    ).select_related('quiz').order_by('-completed_at')

    for attempt in completed_attempts:
        total = attempt.quiz.questions.aggregate(
            total=models.Sum('point')
        )['total']
        attempt.total_points = total or attempt.quiz.questions.count()

    context = {
        'attempts': completed_attempts
    }
    return render(request, 'quiz_app/Student/student_results.html', context)

@student_required
def student_quiz_result_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Try to get any attempt (completed or in progress)
    attempt = Quiz_Attempt.objects.filter(
        student=request.user,
        quiz=quiz
    ).first()  # Returns None if no attempt
     
    # Calculate total points once
    total_points = quiz.questions.aggregate(
        total=models.Sum('point')
    )['total'] or quiz.questions.count()
    percentage = (attempt.score / total_points * 100) if total_points else 0

    # Attach to attempt if exists
    if attempt:
        attempt.total_points = total_points

    context = {
        'quiz': quiz,
        'attempt': attempt,
        'total_points': total_points,
        'percentage': round(percentage, 1),
    }
    return render(request, 'quiz_app/Student/student_quiz_result_detail.html', context)