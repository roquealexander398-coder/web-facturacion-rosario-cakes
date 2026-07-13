from rest_framework import serializers

from .models import Sale, SaleDetail


class SaleDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_code = serializers.CharField(source='product.code', read_only=True)

    class Meta:
        model = SaleDetail
        fields = (
            'id', 'product', 'product_name', 'product_code',
            'quantity', 'price', 'discount', 'total'
        )


class SaleSerializer(serializers.ModelSerializer):
    details = SaleDetailSerializer(many=True, read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Sale
        fields = (
            'id', 'invoice_number', 'client', 'client_name', 'date',
            'subtotal', 'discount', 'tax', 'tax_rate', 'total',
            'payment_method', 'payment_method_display', 'status',
            'status_display', 'notes', 'details', 'created_at'
        )
        read_only_fields = ('invoice_number', 'date', 'created_at')
