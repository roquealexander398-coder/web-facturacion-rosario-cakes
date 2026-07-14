from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id_pastel', 'nombre', 'descripcion', 'categoria',
            'precio_base', 'disponible', 'imagen', 'fecha_actualizacion'
        )
        read_only_fields = ('id_pastel', 'fecha_actualizacion')

