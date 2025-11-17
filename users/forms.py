from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class User_Form(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'Full_name', 'role', 'password1', 'password2']

        labels = {
            'Full_name': 'Full Name',
            "role": 'User Role',
            "username": 'User Name',
            "email": 'Email Address',
            "password1": 'Password',
            "password2": 'Confirm Password',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'Full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
