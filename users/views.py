from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib import messages

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
                login(request, user)
                messages.success(request, "Successfully Logged-In")
                return redirect('')
            else:
                messages.error(request, f'Login Failed!!')