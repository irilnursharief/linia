from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ['name', 'branch', 'prefix', 'is_active']
    list_filter   = ['branch', 'is_active']
    search_fields = ['name', 'prefix']