from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    client_type_display = serializers.CharField(source='get_client_type_display', read_only=True)

    class Meta:
        model = Client
        fields = (
            'id', 'name', 'client_type', 'client_type_display', 'identification',
            'email', 'phone', 'address', 'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')
