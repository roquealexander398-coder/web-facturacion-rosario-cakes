from rest_framework import serializers

from .models import Category, Product, InventoryMovement


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'parent', 'is_active', 'created_at')


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'code', 'name', 'description', 'category', 'category_name',
            'unit', 'price', 'cost', 'stock', 'min_stock', 'max_stock',
            'is_active', 'is_low_stock', 'image', 'created_at'
        )
        read_only_fields = ('created_at',)


class InventoryMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = InventoryMovement
        fields = (
            'id', 'product', 'product_name', 'movement_type', 'quantity',
            'previous_stock', 'new_stock', 'reference', 'notes', 'created_at'
        )
        read_only_fields = ('created_at',)
