from django.urls import reverse
from .models import User


def get_redirect_url_for_role(user):
    if user.is_admin:
        return reverse("admin:index")
    elif user.is_staff_member:
        return reverse("counter-select")
    elif user.is_ticketing:
        return reverse("home")
    elif user.is_tv_display:
        return reverse("display")
    else:
        return reverse("home")
