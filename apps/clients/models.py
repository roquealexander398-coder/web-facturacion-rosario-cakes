from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class Client(models.Model):
    """Modelo de clientes - Mapea a tabla clientes en MySQL"""
    
    PAYMENT_TYPE_CHOICES = [
        ('Efectivo', _('Efectivo')),
        ('Tarjeta', _('Tarjeta')),
        ('Transferencia', _('Transferencia')),
        ('Crédito', _('Crédito')),
    ]
    
    id_cliente = models.AutoField(primary_key=True, db_column='id_cliente')
    nombre = models.CharField(max_length=100, db_column='nombre')
    tipo_pago = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE_CHOICES,
        default='Efectivo',
        db_column='tipo_pago'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True, db_column='fecha_registro')
    telefono = models.CharField(max_length=20, blank=True, null=True, db_column='telefono')
    direccion = models.CharField(max_length=255, blank=True, null=True, db_column='direccion')
    email = models.EmailField(blank=True, null=True, db_column='email')
    
    class Meta:
        db_table = 'clientes'
        ordering = ['-fecha_registro']
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')
        managed = False  # No crear/eliminar tabla
    
    def __str__(self):
        return f"{self.nombre} ({self.id_cliente})"
    
    def get_payment_type_display(self):
        return dict(self.PAYMENT_TYPE_CHOICES).get(self.tipo_pago, self.tipo_pago)