# Django Quiz Application Documentation

## Overview

This is a Django-based quiz application that allows instructors to create quizzes with various question types (MCQ, True/False, Short Answer) and students to take quizzes one question at a time with a timer. It supports role-based access (students and instructors), attempt limiting (one attempt per quiz), scoring, and viewing results.

The app uses Django's authentication system with custom user roles. It includes features like progress saving, auto-submit on timeout, and instructor dashboards for viewing participant results.

**Built with:**
- Django 4.x
- Python 3.14
- Bootstrap for frontend 

**Key Features:**
- User registration and login with roles (Student/Instructor)
- Instructors can create quizzes and add questions
- Students can take quizzes (one question per page, timed)
- Only one attempt per quiz
- Auto-scoring for MCQ and True/False
- Results viewing for students and instructors
- Role-based permissions using custom decorators

Access at: http://127.0.0.1:8000/

## Models

The app has the following models:

### CustomUser (in users/models.py)
- Extends AbstractUser
- Fields: `Full_name` (CharField), `role` (Choices: 'student', 'instructor')
- Used for role-based authentication

### Quiz (in quiz_app/models.py)
- Fields: `user` (FK to CustomUser), `title`, `description`, `created_at`, `duration` (minutes)
- Instructors create quizzes

### Question (in quiz_app/models.py)
- Fields: `quiz` (FK to Quiz), `question_type` (Choices: 'MCQ', 'TF', 'SA'), `question_text`, `option1-4` (for MCQ), `correct_option`, `answer_text_SA`, `answer_text_TF`, `point` (default 1)
- Supports multiple question types

### Quiz_Attempt (in quiz_app/models.py)
- Fields: `student` (FK to CustomUser), `quiz` (FK to Quiz), `started_at`, `completed_at`, `score`, `time_remaining`
- Tracks student attempts (one per quiz, enforced in views)

### Student_Answer (in quiz_app/models.py)
- Fields: `attempt` (FK to Quiz_Attempt), `question` (FK to Question), `selected_option`, `answer_text`
- Stores answers for each question in an attempt

## Forms

### User_Form (in users/forms.py)
- Extends UserCreationForm
- Fields: username, email, Full_name, role, passwords
- Custom validation for unique email

### Quiz_Form (in quiz_app/forms.py, assumed from code)
- ModelForm for Quiz: title, description, duration

### Question_Form (in quiz_app/forms.py, assumed)
- ModelForm for Question: all fields including type, options, correct answers, point

### Answer_Form (in quiz_app/forms.py, assumed)
- Dynamic form for student answers based on question type (radio for MCQ/TF, textarea for SA)

## Views

### Users App (users/views.py)
- **Index_View**: Handles login (GET/POST)
- **Register_View**: Handles registration (GET/POST)
- **logout**: Logs out user

### Quiz App (quiz_app/views.py)
- **stu_home**: Student dashboard - list quizzes
- **inst_home**: Instructor dashboard - list own quizzes
- **Create_QuizView**: Create new quiz (class-based)
- **Add_QuestionView**: Add questions to quiz (class-based)
- **view_qiuz_instructor**: View quiz details for instructor
- **quiz_instruction**: Show quiz instructions
- **start_quiz**: Start/resume quiz (enforces one attempt)
- **quiz_question**: Display one question, handle answers, navigation, timer
- **quiz_finish**: Finish quiz, calculate score, show result
- **student_results**: List all student's completed quizzes
- **quiz_participants**: Instructor views all participants and scores for one quiz
- **student_quiz_result_detail**: Student views detailed result for one quiz

Custom decorators: `instructor_required`, `student_required` (in quiz_app/decourators.py)

## URLs

### Users App (users/urls.py)
- `/`: Index (login)
- `/register/`: Registration
- `/logout/`: Logout

### Quiz App (quiz_app/urls.py)
- `/student/home/`: Student home
- `/instructor/home/`: Instructor home
- `/instructor/create_quiz/`: Create quiz
- `/instructor/add_question/<quiz_id>/`: Add question
- `/instructor/view_quiz/<quiz_id>/`: View quiz
- `/student/quiz_instruction/<quiz_id>/`: Quiz instructions
- `/student/quiz/<quiz_id>/start/`: Start quiz
- `/student/quiz/<quiz_id>/question/<question_id>/`: Question page
- `/student/quiz/attempt/<attempt_id>/finish/`: Finish quiz
- `/student/results/`: All student results
- `/instructor/quiz/<quiz_id>/participants/`: Participants list
- `/student/quiz/<quiz_id>/result/`: Detailed result for one quiz

## Templates

- **Base Template**: `base/base.html` (navbar with role-based links)
- **Login/Register**: `users/index.html`, `users/register.html`
- **Student**: `stu_home.html` (quiz list), `start_quiz.html` (instructions), `quiz_question.html` (one question), `quiz_result.html` (result), `student_results.html` (all results), `student_quiz_result_detail.html` (one quiz detail)
- **Instructor**: `inst_home.html` (quiz list), `create_quiz.html`, `add_question.html`, `view_quiz_instructor.html`, `quiz_participants.html` (participants list)

Templates use Bootstrap for styling.

## Permissions & Security

- Role-based access using custom decorators
- Instructors can only view/edit own quizzes
- Students can only view own results
- One attempt per quiz enforced in `start_quiz`
- Timer & auto-submit in `quiz_question`

## How to Test

1. Register as Instructor → Create quiz → Add questions
2. Register as Student → Take quiz → See result
3. As Instructor → View participants & scores
4. As Student → View my results → Click to see detailed result

**Last Updated**: November 23, 2025

Contact for questions: [Atiemo-Keseku David Obeng/datiemokeseku16@gmil.com]