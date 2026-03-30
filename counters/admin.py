from django.contrib import admin
from .models import Counter


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ["number", "branch", "service", "staff", "status"]
    list_filter = ["branch", "status"]
    search_fields = ["number"]
