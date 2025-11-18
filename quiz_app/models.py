from django.db import models

# Create your models here.
class  Quiz(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    duration = models.IntegerField(default=5, help_text="Duration in minutes")

    def __str__(self):
        return self.title
    
class Question(models.Model):
    Question_types = [
        ('MCQ', 'Multiple Choice Question'),
        ('TF', 'True/False Question'),
        ('SA', 'Short Answer Question'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=3, choices=Question_types, default='MCQ')
    question_text = models.TextField(max_length=300)
    option1 = models.CharField(max_length=150, blank=True, null=True)
    option2 = models.CharField(max_length=150, blank=True, null=True)
    option3 = models.CharField(max_length=150, blank=True, null=True)
    option4 = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f'{self.quiz.title} - {self.question_text}'

class Answer(models.Model):
    Options = [
      ('A', 'Option 1'),
      ('B', 'Option 2'),
      ('C', 'Option 3'),
      ('D', 'Option 4'),
    ]

    question_text = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    correct_option = models.CharField(max_length=1, choices=Options, blank=True, null=True)
    answer_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.question_text} - {self.correct_option}{self.answer_text}'