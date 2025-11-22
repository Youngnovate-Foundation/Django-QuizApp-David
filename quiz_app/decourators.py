# quiz_app/utils.py
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps

def instructor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # or your login url name
        
        if request.user.role != 'instructor':
            raise PermissionDenied("You don't have permission to access this page.")
            # Or redirect to student home:
            # return redirect('stu_home')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role != 'student':
            raise PermissionDenied("Only students can access this page.")
            # Or redirect to instructor home:
            # return redirect('inst_home')
        
        return view_func(request, *args, **kwargs)
    return wrapper