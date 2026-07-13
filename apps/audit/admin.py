from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'record_id', 'created_at')
    list_filter = ('action', 'model_name')
    search_fields = ('user__username', 'model_name')
    readonly_fields = ('created_at',)
