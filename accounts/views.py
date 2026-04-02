from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .services import get_redirect_url_for_role


def login_view(request):
    if request.user.is_authenticated:
        return redirect(get_redirect_url_for_role(request.user))

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # THE FIX: Check for branch assignment before completing login
            if not user.branch and not user.is_superuser:
                messages.error(
                    request,
                    "Your account is not assigned to any branch. Please contact the administrator.",
                )
                return redirect("login")

            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(get_redirect_url_for_role(user))

        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect("login")
    return render(request, "accounts/logout.html")
