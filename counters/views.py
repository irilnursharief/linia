from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Counter
from queueing.models import Ticket


def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff_member:
            messages.error(request, "Access denied. Staff only.")
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
@staff_required
def counter_dashboard(request):
    counter = Counter.objects.filter(
        staff=request.user, status=Counter.Status.OPEN
    ).first()

    current_ticket = None
    waiting_tickets = []

    if counter:
        current_ticket = Ticket.objects.filter(
            counter=counter, status=Ticket.Status.SERVING
        ).first()

        waiting_tickets = Ticket.objects.filter(
            branch=counter.branch, service=counter.service, status=Ticket.Status.WAITING
        )

    context = {
        "counter": counter,
        "current_ticket": current_ticket,
        "waiting_tickets": waiting_tickets,
    }
    return render(request, "counters/dashboard.html", context)


@login_required
@staff_required
def call_next(request):
    if request.method == "POST":
        counter = Counter.objects.filter(
            staff=request.user, status=Counter.Status.OPEN
        ).first()

        if not counter:
            messages.error(request, "No open counter assigned to you.")
            return redirect("counter-dashboard")

        # Complete current serving ticket first
        Ticket.objects.filter(counter=counter, status=Ticket.Status.SERVING).update(
            status=Ticket.Status.COMPLETED
        )

        # Get next ticket by priority then created_at
        next_ticket = Ticket.objects.filter(
            branch=counter.branch, service=counter.service, status=Ticket.Status.WAITING
        ).first()

        if next_ticket:
            next_ticket.status = Ticket.Status.SERVING
            next_ticket.counter = counter
            next_ticket.called_at = timezone.now()
            next_ticket.save()
            messages.success(request, f"Now serving {next_ticket.ticket_number}")
        else:
            messages.info(request, "No tickets waiting.")

    return redirect("counter-dashboard")


@login_required
@staff_required
def recall(request):
    if request.method == "POST":
        counter = Counter.objects.filter(
            staff=request.user, status=Counter.Status.OPEN
        ).first()

        if counter:
            current_ticket = Ticket.objects.filter(
                counter=counter, status=Ticket.Status.SERVING
            ).first()

            if current_ticket:
                current_ticket.called_at = timezone.now()
                current_ticket.save()
                messages.success(request, f"Recalled {current_ticket.ticket_number}")
            else:
                messages.info(request, "No ticket currently being served.")

    return redirect("counter-dashboard")


@login_required
@staff_required
def no_show(request):
    if request.method == "POST":
        counter = Counter.objects.filter(
            staff=request.user, status=Counter.Status.OPEN
        ).first()

        if counter:
            current_ticket = Ticket.objects.filter(
                counter=counter, status=Ticket.Status.SERVING
            ).first()

            if current_ticket:
                current_ticket.status = Ticket.Status.NO_SHOW
                current_ticket.save()
                messages.success(
                    request, f"Marked {current_ticket.ticket_number} as no show."
                )

    return redirect("counter-dashboard")


@login_required
@staff_required
def complete(request):
    if request.method == "POST":
        counter = Counter.objects.filter(
            staff=request.user, status=Counter.Status.OPEN
        ).first()

        if counter:
            current_ticket = Ticket.objects.filter(
                counter=counter, status=Ticket.Status.SERVING
            ).first()

            if current_ticket:
                current_ticket.status = Ticket.Status.COMPLETED
                current_ticket.save()
                messages.success(request, f"{current_ticket.ticket_number} completed.")

    return redirect("counter-dashboard")
