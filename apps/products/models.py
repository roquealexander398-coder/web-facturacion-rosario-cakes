from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    """Modelo de categorías de productos"""
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Nombre'))
    description = models.TextField(blank=True, verbose_name=_('Descripción'))
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name=_('Categoría Padre')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Activa'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name = _('Categoría')
        verbose_name_plural = _('Categorías')
    
    def __str__(self):
        return self.name
    
    @property
    def full_name(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

class Product(models.Model):
    """Modelo de productos"""
    
    class Unit(models.TextChoices):
        UNIT = 'UNIT', _('Unidad')
        KG = 'KG', _('Kilogramo')
        LB = 'LB', _('Libra')
        L = 'L', _('Litro')
        ML = 'ML', _('Mililitro')
        M = 'M', _('Metro')
        CM = 'CM', _('Centímetro')
    
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Código'))
    name = models.CharField(max_length=200, verbose_name=_('Nombre'))
    description = models.TextField(blank=True, verbose_name=_('Descripción'))
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('Categoría')
    )
    unit = models.CharField(
        max_length=10,
        choices=Unit.choices,
        default=Unit.UNIT,
        verbose_name=_('Unidad de Medida')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Precio de Venta')
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Costo')
    )
    stock = models.PositiveIntegerField(default=0, verbose_name=_('Stock Actual'))
    min_stock = models.PositiveIntegerField(default=5, verbose_name=_('Stock Mínimo'))
    max_stock = models.PositiveIntegerField(default=100, verbose_name=_('Stock Máximo'))
    is_active = models.BooleanField(default=True, verbose_name=_('Activo'))
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name=_('Imagen'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='products_created'
    )
    
    class Meta:
        db_table = 'products'
        ordering = ['name']
        verbose_name = _('Producto')
        verbose_name_plural = _('Productos')
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def is_low_stock(self):
        return self.stock <= self.min_stock
    
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