from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import AuditLog
from .serializers import AuditLogSerializer


@login_required
def audit_logs(request):
    logs = AuditLog.objects.select_related('user').order_by('-created_at')[:100]
    action = request.GET.get('action')
    if action:
        logs = logs.filter(action=action)
    return render(request, 'audit/logs.html', {'logs': logs})


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'model_name', 'user']
    search_fields = ['model_name', 'user__username']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
