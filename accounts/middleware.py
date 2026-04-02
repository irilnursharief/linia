# accounts/middleware.py
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from counters.models import Counter  # Adjust this import based on your app name


class BranchSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # We only apply this logic to staff, NOT to Superusers
            if request.user.is_staff_member and not request.user.is_superuser:

                # If a staff member loses their branch (Mid-Shift Fix)
                if not request.user.branch:
                    # 1. Cleanup: Close their counter so it's not "occupied" by a ghost
                    Counter.objects.filter(
                        staff=request.user, status=Counter.Status.OPEN
                    ).update(staff=None, status=Counter.Status.CLOSED)

                    # 2. Security: Log them out
                    messages.error(
                        request, "Access denied: No branch assigned to your account."
                    )
                    logout(request)
                    return redirect("login")

        return self.get_response(request)
