from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from branches.models import Branch
from counters.models import Counter
from queueing.models import Ticket


def get_display_context(branch_id):
    """Helper to keep logic DRY"""
    branch = get_object_or_404(Branch, id=branch_id)

    # 1. Tickets currently being called/served
    serving_tickets = (
        Ticket.objects.filter(branch=branch, status=Ticket.Status.SERVING)
        .select_related("counter", "service")
        .order_by("-called_at")[:5]
    )

    # 2. Counter availability
    counters = Counter.objects.filter(branch=branch).order_by("number")

    # 3. People waiting per service
    waiting_stats = (
        Ticket.objects.filter(branch=branch, status=Ticket.Status.WAITING)
        .values("service__name")
        .annotate(total=Count("id"))
    )

    return {
        "branch": branch,
        "serving_tickets": serving_tickets,
        "counters": counters,
        "waiting_stats": waiting_stats,
    }


def display_main(request, branch_id):
    context = get_display_context(branch_id)
    return render(request, "display/main_display.html", context)


def display_update(request, branch_id):
    context = get_display_context(branch_id)
    return render(request, "display/partials/board.html", context)
