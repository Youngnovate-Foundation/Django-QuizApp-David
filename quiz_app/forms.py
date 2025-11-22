from django import forms
from .models import Quiz, Question

class Quiz_Form(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'duration']
        labels = {
            'title': 'Quiz Title',
            'description': 'Quiz Description',
            'duration': 'Duration',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quiz title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter quiz description', 'rows': 4}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter duration in minutes'}),
        }

class Question_Form(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_type', 'question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option', 'answer_text_SA', 'answer_text_TF']
        labels = {
            # 'quiz': 'Select Quiz',
            'question_type': 'Question Type',
            'question_text': 'Question Text',
            'option1': 'Option A',
            'option2': 'Option B',
            'option3': 'Option C',
            'option4': 'Option D',
            'correct_option': 'Correct Option (For MCQ)',
            'answer_text_SA': 'Answer Text (For Short Answer Questions)',
            'answer_text_TF': 'Answer (For True/False Questions)',
            'point': 'Mark fo question',
        }

        widgets ={
            # 'quiz': forms.Select(attrs={'class': 'form-select'}),
            'question_type': forms.Select(attrs={'class': 'form-select'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter question text', 'rows': 3}),
            'option1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter option A (For only MCQ)'}),
            'option2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter option B (For only MCQ)'}),
            'option3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter option C (For only MCQ)'}),
            'option4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter option D (For only MCQ)'}),
            'correct_option': forms.Select(attrs={'class': 'form-select'}),
            'answer_text_SA': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter answer text', 'rows': 3}),
            'answer_text_TF': forms.Select(attrs={'class': 'form-select'}),
            'point': forms.NumberInput(attrs={'class': 'form-control','default':1}),
        }
