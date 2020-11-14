from functools import wraps

from django.shortcuts import redirect


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("users:login")
            if request.user.role not in roles:
                return redirect("users:login")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
