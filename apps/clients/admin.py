from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_pago', 'telefono', 'email', 'fecha_registro')
    list_filter = ('tipo_pago', 'fecha_registro')
    search_fields = ('nombre', 'email', 'telefono')
    fields = ('nombre', 'tipo_pago', 'telefono', 'direccion', 'email', 'fecha_registro')
    readonly_fields = ('id_cliente', 'fecha_registro')

