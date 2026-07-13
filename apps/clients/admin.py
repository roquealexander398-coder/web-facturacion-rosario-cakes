from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'identification', 'client_type', 'phone', 'is_active')
    list_filter = ('client_type', 'is_active')
    search_fields = ('name', 'identification', 'email')
