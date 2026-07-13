from rest_framework import serializers

from .models import Provider, ProviderProduct


class ProviderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ProviderProduct
        fields = (
            'id', 'provider', 'product', 'product_name', 'provider_code',
            'price', 'delivery_time', 'is_preferred', 'created_at'
        )


class ProviderSerializer(serializers.ModelSerializer):
    provider_type_display = serializers.CharField(source='get_provider_type_display', read_only=True)
    products_count = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Provider
        fields = (
            'id', 'name', 'provider_type', 'provider_type_display', 'rnc',
            'email', 'phone', 'address', 'contact_person', 'contact_phone',
            'website', 'notes', 'is_active', 'products_count', 'created_at'
        )
        read_only_fields = ('created_at',)
