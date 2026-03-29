from django.db import transaction
from .models import Ticket
from branches.models import Branch
from services.models import Service


def generate_ticket_number(service: Service, branch: Branch) -> str:
    last_ticket = Ticket.objects.filter(
        branch=branch,
        service=service,
    ).order_by('-created_at').first()

    if last_ticket:
        last_number = int(last_ticket.ticket_number.split('-')[1])
        new_number  = last_number + 1
    else:
        new_number = 1

    return f"{service.prefix}-{str(new_number).zfill(3)}"


@transaction.atomic
def create_ticket(
    *,
    branch: Branch,
    service: Service,
    client_type: str,
    client=None,
    is_pre_registered: bool = False
) -> Ticket:
    ticket_number = generate_ticket_number(service=service, branch=branch)

    ticket = Ticket(
        branch=branch,
        service=service,
        client=client,
        ticket_number=ticket_number,
        client_type=client_type,
        is_pre_registered=is_pre_registered,
    )
    ticket.full_clean()
    ticket.save()

    return ticket