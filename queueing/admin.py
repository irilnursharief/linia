from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display  = ['ticket_number', 'branch', 'service', 'client_type', 'priority', 'status', 'created_at']
    list_filter   = ['branch', 'service', 'client_type', 'status']
    search_fields = ['ticket_number']