from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please login to continue.")
                return redirect("login")
            if request.user.role not in roles:
                messages.error(request, "You do not have access to this page.")
                return redirect("login")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
