from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display  = ['username', 'email', 'role', 'branch', 'is_active']
    list_filter   = ['role', 'branch', 'is_active']
    search_fields = ['username', 'email']
    fieldsets     = UserAdmin.fieldsets + (
        ('Role & Branch', {'fields': ('role', 'branch')}),
    )