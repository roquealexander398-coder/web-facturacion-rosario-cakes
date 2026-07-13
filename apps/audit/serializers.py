from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True, default='Sistema')
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = AuditLog
        fields = (
            'id', 'user', 'username', 'action', 'action_display',
            'model_name', 'record_id', 'data_before', 'data_after',
            'ip_address', 'user_agent', 'created_at'
        )
