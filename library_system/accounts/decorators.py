from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if hasattr(request.user, 'userprofile'):
                user_role = request.user.userprofile.role
                if user_role in roles:
                    return view_func(request, *args, **kwargs)

            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        return wrapper
    return decorator
