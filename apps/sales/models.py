from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Sale(models.Model):
    """Modelo de pedidos/ventas - Mapea a tabla pedidos en MySQL"""
    
    ORDER_STATUS_CHOICES = [
        ('Pendiente', _('Pendiente')),
        ('En Preparación', _('En Preparación')),
        ('Listo', _('Listo')),
        ('Entregado', _('Entregado')),
        ('Cancelado', _('Cancelado')),
    ]
    
    SIZE_CHOICES = [
        ('Pequeño', _('Pequeño')),
        ('Mediano', _('Mediano')),
        ('Grande', _('Grande')),
        ('Extra Grande', _('Extra Grande')),
    ]
    
    id_pedido = models.AutoField(primary_key=True, db_column='id_pedido')
    id_cliente = models.ForeignKey(
        'clients.Client',
        on_delete=models.PROTECT,
        db_column='id_cliente',
        related_name='pedidos'
    )
    id_pastel = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        db_column='id_pastel',
        related_name='pedidos'
    )
    cantidad = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        db_column='cantidad'
    )
    tamaño = models.CharField(
        max_length=20,
        choices=SIZE_CHOICES,
        default='Mediano',
        db_column='tamaño'
    )
    fecha_pedido = models.DateTimeField(db_column='fecha_pedido')
    fecha_entrega = models.DateTimeField(db_column='fecha_entrega')
    observaciones = models.TextField(blank=True, null=True, db_column='observaciones')
    estado = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='Pendiente',
        db_column='estado'
    )
    
    # Campos adicionales para compatibilidad
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pedidos'
        ordering = ['-fecha_pedido']
        verbose_name = _('Pedido')
        verbose_name_plural = _('Pedidos')
        managed = False  # No crear/eliminar tabla
    
    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.id_cliente.nombre}"
    
    def get_estado_display(self):
        return dict(self.ORDER_STATUS_CHOICES).get(self.estado, self.estado)
    
    def get_tamaño_display(self):
        return dict(self.SIZE_CHOICES).get(self.tamaño, self.tamaño)
    
    @property
    def total_price(self):
        """Calcular el precio total del pedido"""
        return self.id_pastel.precio_base * self.cantidad


class Payment(models.Model):
    """Modelo de pagos - Mapea a tabla pagos en MySQL"""
    
    PAYMENT_METHOD_CHOICES = [
        ('Efectivo', _('Efectivo')),
        ('Tarjeta', _('Tarjeta')),
        ('Transferencia', _('Transferencia')),
        ('Crédito', _('Crédito')),
    ]
    
    STATUS_CHOICES = [
        ('Pendiente', _('Pendiente')),
        ('Completado', _('Completado')),
        ('Cancelado', _('Cancelado')),
    ]
    
    id_pago = models.AutoField(primary_key=True, db_column='id_pago')
    id_pedido = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        db_column='id_pedido',
        related_name='pagos'
    )
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        db_column='monto'
    )
    metodo = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        db_column='metodo'
    )
    estado = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Completado',
        db_column='estado'
    )
    fecha_pago = models.DateTimeField(auto_now_add=True, db_column='fecha_pago')
    
    class Meta:
        db_table = 'pagos'
        ordering = ['-fecha_pago']
        verbose_name = _('Pago')
        verbose_name_plural = _('Pagos')
        managed = False  # No crear/eliminar tabla
    
    def __str__(self):
        return f"Pago {self.id_pago} - ${self.monto}"
    
    def get_metodo_display(self):
        return dict(self.PAYMENT_METHOD_CHOICES).get(self.metodo, self.metodo)
    
    def get_estado_display(self):
        return dict(self.STATUS_CHOICES).get(self.estado, self.estado)


class Invoice(models.Model):
    """Modelo de facturas - Mapea a tabla facturas en MySQL"""
    
    INVOICE_STATUS_CHOICES = [
        ('Válida', _('Válida')),
        ('Anulada', _('Anulada')),
    ]
    
    id_factura = models.AutoField(primary_key=True, db_column='id_factura')
    id_pedido = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        db_column='id_pedido',
        related_name='facturas'
    )
    ncf = models.CharField(max_length=20, unique=True, db_column='ncf')
    monto_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        db_column='monto_total'
    )
    fecha_emision = models.DateTimeField(auto_now_add=True, db_column='fecha_emision')
    estado = models.CharField(
        max_length=20,
        choices=INVOICE_STATUS_CHOICES,
        default='Válida',
        db_column='estado'
    )
    
    class Meta:
        db_table = 'facturas'
        ordering = ['-fecha_emision']
        verbose_name = _('Factura')
        verbose_name_plural = _('Facturas')
        managed = False  # No crear/eliminar tabla
    
    def __str__(self):
        return f"Factura {self.ncf} - ${self.monto_total}"
    
    def get_estado_display(self):
        return dict(self.INVOICE_STATUS_CHOICES).get(self.estado, self.estado)
