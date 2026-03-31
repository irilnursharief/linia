from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import GetTicketForm, PreRegisterForm
from .services import create_ticket
from branches.models import Branch
from services.models import Service
from django.http import HttpResponse
from accounts.decorators import role_required


@role_required("ticketing")
def home(request):
    branches = Branch.objects.filter(is_active=True)
    return render(request, "queueing/home.html", {"branches": branches})


@role_required("ticketing")
def get_ticket(request):
    if request.method == "POST":
        form = GetTicketForm(request.POST)
        if form.is_valid():
            ticket = create_ticket(
                branch=form.cleaned_data["branch"],
                service=form.cleaned_data["service"],
                client_type=form.cleaned_data["client_type"],
                client=request.user if request.user.is_authenticated else None,
            )
            messages.success(request, f"Your ticket number is {ticket.ticket_number}")
            return redirect("ticket-status", pk=ticket.pk)
    else:
        form = GetTicketForm()

    return render(request, "queueing/get_ticket.html", {"form": form})


def load_services(request):
    branch_id = request.GET.get("branch")

    services = Service.objects.filter(branch_id=branch_id, is_active=True)

    return render(
        request, "queueing/partials/service_options.html", {"services": services}
    )


@role_required("ticketing")
def pre_register(request):
    if request.method == "POST":
        form = PreRegisterForm(request.POST)
        if form.is_valid():
            ticket = create_ticket(
                branch=form.cleaned_data["branch"],
                service=form.cleaned_data["service"],
                client_type=form.cleaned_data["client_type"],
                client=request.user if request.user.is_authenticated else None,
                is_pre_registered=True,
            )
            messages.success(
                request,
                f"Pre-registration successful! Your ticket is {ticket.ticket_number}",
            )
            return redirect("ticket-status", pk=ticket.pk)
    else:
        form = PreRegisterForm()

    return render(request, "queueing/pre_register.html", {"form": form})


def ticket_status(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    waiting_ahead = Ticket.objects.filter(
        branch=ticket.branch,
        service=ticket.service,
        status=Ticket.Status.WAITING,
        priority__lte=ticket.priority,
        created_at__lt=ticket.created_at,
    ).count()

    context = {
        "ticket": ticket,
        "waiting_ahead": waiting_ahead,
    }
    return render(request, "queueing/ticket_status.html", context)
