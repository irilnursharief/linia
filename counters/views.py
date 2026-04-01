from urllib import request

from django.core import paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Counter
from queueing.models import Ticket
from accounts.decorators import role_required
from services.models import Service
from django.db.models import Avg, Count
from datetime import datetime, date
from django.core.paginator import Paginator
from django.db.models import F, ExpressionWrapper, DurationField, Avg


@login_required
@role_required("staff")
def counter_dashboard(request):
    counter = Counter.objects.filter(
        staff=request.user, status=Counter.Status.OPEN
    ).first()

    if not counter:
        messages.warning(request, "Please select a counter first.")
        return redirect("counter-select")

    # Handle service switch
    if request.method == "POST" and "switch_service" in request.POST:
        service_id = request.POST.get("service_id")
        service = Service.objects.filter(
            id=service_id, branch=counter.branch, is_active=True
        ).first()

        if service:
            counter.service = service
            counter.save()
            messages.success(request, f"Switched to {service.name}")
        return redirect("counter-dashboard")

    current_ticket = None
    waiting_tickets = []

    current_ticket = Ticket.objects.filter(
        counter=counter, status=Ticket.Status.SERVING
    ).first()

    waiting_tickets = Ticket.objects.filter(
        branch=counter.branch, service=counter.service, status=Ticket.Status.WAITING
    )

    # Get all services for this branch for the switcher
    branch_services = Service.objects.filter(branch=counter.branch, is_active=True)

    context = {
        "counter": counter,
        "current_ticket": current_ticket,
        "waiting_tickets": waiting_tickets,
        "branch_services": branch_services,
    }
    return render(request, "counters/dashboard.html", context)


@login_required
@role_required("staff")
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
@role_required("staff")
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
@role_required("staff")
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
@role_required("staff")
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
                current_ticket.served_at = timezone.now()  # ← add this
                current_ticket.save()

                if current_ticket.handling_time:
                    messages.success(
                        request,
                        f"✅ {current_ticket.ticket_number} completed. "
                        f"Handling time: {current_ticket.handling_time}",
                    )
                else:
                    messages.success(
                        request, f"{current_ticket.ticket_number} completed."
                    )

    return redirect("counter-dashboard")


@login_required
@role_required("staff")
def counter_select(request):
    branch = request.user.branch

    if not branch:
        messages.error(request, "You are not assigned to any branch.")
        return redirect("login")

    if request.method == "POST":
        counter_id = request.POST.get("counter_id")

        Counter.objects.filter(staff=request.user, status=Counter.Status.OPEN).update(
            staff=None, status=Counter.Status.CLOSED
        )

        if counter_id:
            counter = Counter.objects.filter(
                id=counter_id,
                branch=branch,
            ).first()

            if counter:
                counter.staff = request.user
                counter.status = Counter.Status.OPEN
                counter.save()
                messages.success(request, f"You are now at counter {counter.number}.")
                return redirect("counter-dashboard")

    available_counters = Counter.objects.filter(
        branch=branch,
    ).order_by("number")

    my_counter = Counter.objects.filter(
        staff=request.user, status=Counter.Status.OPEN
    ).first()

    context = {
        "available_counters": available_counters,
        "my_counter": my_counter,
        "branch": branch,
    }
    return render(request, "counters/counter_select.html", context)


@login_required
@role_required("staff")
def counter_reports(request):
    tickets = (
        Ticket.objects.filter(
            counter__staff=request.user,
            status=Ticket.Status.COMPLETED,
        )
        .select_related("service", "branch", "counter")
        .order_by("-served_at")
    )

    client_type = request.GET.get("client_type", "")
    service_id = request.GET.get("service", "")
    date_filter = request.GET.get("date", "")

    if client_type:
        tickets = tickets.filter(client_type=client_type)

    if service_id:
        tickets = tickets.filter(service__id=service_id)

    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
            tickets = tickets.filter(served_at__date=filter_date)
        except ValueError:
            pass

    tickets_with_time = tickets.filter(
        called_at__isnull=False,
        served_at__isnull=False,
    ).annotate(
        handling_time_duration=ExpressionWrapper(
            F("served_at") - F("called_at"), output_field=DurationField()
        )
    )

    avg_duration = tickets_with_time.aggregate(avg_time=Avg("handling_time_duration"))[
        "avg_time"
    ]

    def format_duration(duration):
        if not duration:
            return None

        total_seconds = int(duration.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"

    average_aht = format_duration(avg_duration)

    total_served = tickets.count()

    branch_services = Service.objects.filter(
        branch=request.user.branch,
        is_active=True,
    )

    per_page = request.GET.get("per_page", 10)

    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10

    paginator = Paginator(tickets, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "tickets": page_obj,
        "page_obj": page_obj,
        "total_served": total_served,
        "branch_services": branch_services,
        "client_types": Ticket.ClientType.choices,
        "selected_client_type": client_type,
        "selected_service": service_id,
        "selected_date": date_filter,
        "average_aht": average_aht,
    }

    return render(request, "counters/reports.html", context)
