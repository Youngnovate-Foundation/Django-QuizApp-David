from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from .forms import User_Form


# Create your views here.
class Index_View(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'users/index.html', {'login_form': login_form})
    
    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                user.refresh_from_db()
                login(request, user)
                if user.role == 'instructor':
                    messages.success(request, "Successfully Logged-In as Instructor")
                    return redirect('instructor_home')
                else:
                    messages.success(request, "Successfully Logged-In as Student")
                    return redirect('student_home')
            else:
                messages.error(request, f'Login Failed!!')
                return render(request, 'users/index.html', {'login_form': login_form})
        else:
            messages.error(request, f'Login Failed!!')
            return render(request, 'users/index.html', {'login_form': login_form})

class Register_View(View):
    def get(self, request):
        registraton_form = User_Form()
        return render(request, 'users/register.html', {'registraton_form':registraton_form})
    
    def post(self, request):
        registraton_form = User_Form(data=request.POST)
        if registraton_form.is_valid():
            user = registraton_form.save()
            user.refresh_from_db()
            login(request, user)
            if user.role == 'instructor':
                messages.success(request, "Successfully Logged-In as Instructor")
                return redirect('instructor_home')
            else:
                messages.success(request, "Successfully Logged-In as Student")
                return redirect('student_home')
        else:
            messages.error(request, "Registration Failed. Please try again.")
            return render(request, 'users/register.html', {'registraton_form':registraton_form})
        
def logout(request):
    logout(request)
    return redirect('index')