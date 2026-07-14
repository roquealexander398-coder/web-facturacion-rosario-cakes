from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    """Modelo de productos/pasteles - Mapea a tabla pasteles en MySQL"""
    
    CATEGORY_CHOICES = [
        ('Cumpleaños', _('Cumpleaños')),
        ('Boda', _('Boda')),
        ('Celebración', _('Celebración')),
        ('Infantil', _('Infantil')),
        ('Personalizado', _('Personalizado')),
        ('Postres', _('Postres')),
    ]
    
    id_pastel = models.AutoField(primary_key=True, db_column='id_pastel')
    nombre = models.CharField(max_length=100, db_column='nombre')
    descripcion = models.CharField(max_length=255, blank=True, null=True, db_column='descripcion')
    precio_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        db_column='precio_base'
    )
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        blank=True,
        db_column='categoria'
    )
    disponible = models.BooleanField(default=True, db_column='disponible')
    imagen = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        db_column='imagen'
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True, db_column='fecha_actualizacion')
    
    # Campos adicionales para compatibilidad
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pasteles'
        ordering = ['nombre']
        verbose_name = _('Pastel/Producto')
        verbose_name_plural = _('Pasteles/Productos')
        managed = False  # No crear/eliminar tabla
    
    def __str__(self):
        return f"{self.nombre} (${self.precio_base})"
    
    @property
    def name(self):
        """Compatibilidad con modelos antiguos"""
        return self.nombre
    
    @property
    def price(self):
        """Compatibilidad con modelos antiguos"""
        return self.precio_base
    
    def get_categoria_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.categoria, self.categoria)

    
    @property
    def is_out_of_stock(self):
        return self.stock == 0
    
    def update_stock(self, quantity, operation='add'):
        """Actualizar stock con control de operación"""
        if operation == 'add':
            if self.stock + quantity > self.max_stock:
                raise ValueError(f"Stock máximo excedido: {self.max_stock}")
            self.stock += quantity
        elif operation == 'subtract':
            if self.stock - quantity < 0:
                raise ValueError("Stock insuficiente")
            self.stock -= quantity
        self.save()
        return self.stock

class InventoryMovement(models.Model):
    """Modelo de movimientos de inventario"""
    
    class MovementType(models.TextChoices):
        PURCHASE = 'PURCHASE', _('Compra')
        SALE = 'SALE', _('Venta')
        RETURN = 'RETURN', _('Devolución')
        ADJUSTMENT = 'ADJUSTMENT', _('Ajuste')
        TRANSFER = 'TRANSFER', _('Transferencia')
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='movements',
        verbose_name=_('Producto')
    )
    movement_type = models.CharField(
        max_length=10,
        choices=MovementType.choices,
        verbose_name=_('Tipo de Movimiento')
    )
    quantity = models.PositiveIntegerField(verbose_name=_('Cantidad'))
    previous_stock = models.PositiveIntegerField(verbose_name=_('Stock Anterior'))
    new_stock = models.PositiveIntegerField(verbose_name=_('Nuevo Stock'))
    reference = models.CharField(max_length=100, blank=True, verbose_name=_('Referencia'))
    notes = models.TextField(blank=True, verbose_name=_('Observaciones'))
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='inventory_movements'
    )
    
    class Meta:
        db_table = 'inventory_movements'
        ordering = ['-created_at']
        verbose_name = _('Movimiento de Inventario')
        verbose_name_plural = _('Movimientos de Inventario')
    
    def __str__(self):
        return f"{self.product.name} - {self.movement_type} - {self.quantity}"