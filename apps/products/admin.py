from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_base', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre', 'descripcion')
    fields = ('nombre', 'descripcion', 'categoria', 'precio_base', 'disponible', 'imagen')

