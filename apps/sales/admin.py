from django.contrib import admin

from .models import Sale, Payment, Invoice


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id_pedido', 'id_cliente', 'cantidad', 'estado', 'fecha_pedido')
    list_filter = ('estado', 'tamaño')
    search_fields = ('id_cliente__nombre', 'id_pastel__nombre')
    fields = ('id_cliente', 'id_pastel', 'cantidad', 'tamaño', 'fecha_pedido', 'fecha_entrega', 'observaciones', 'estado')
    readonly_fields = ('id_pedido',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id_pago', 'id_pedido', 'monto', 'metodo', 'estado', 'fecha_pago')
    list_filter = ('metodo', 'estado')
    search_fields = ('id_pedido__id_cliente__nombre',)
    readonly_fields = ('id_pago', 'fecha_pago')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id_factura', 'ncf', 'monto_total', 'estado', 'fecha_emision')
    list_filter = ('estado',)
    search_fields = ('ncf', 'id_pedido__id_cliente__nombre')
    readonly_fields = ('id_factura', 'fecha_emision')

