from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    ]
    Full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='student')

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return f'{self.username} - {self.role}'