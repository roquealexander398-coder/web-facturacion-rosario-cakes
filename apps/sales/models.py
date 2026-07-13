from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Sale(models.Model):
    """Modelo de ventas/facturación"""
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pendiente')
        PAID = 'PAID', _('Pagada')
        CANCELLED = 'CANCELLED', _('Cancelada')
        REFUNDED = 'REFUNDED', _('Reembolsada')
    
    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', _('Efectivo')
        CARD = 'CARD', _('Tarjeta')
        TRANSFER = 'TRANSFER', _('Transferencia')
        CHECK = 'CHECK', _('Cheque')
        ONLINE = 'ONLINE', _('Pago en Línea')
    
    invoice_number = models.CharField(max_length=20, unique=True, verbose_name=_('Número de Factura'))
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.PROTECT,
        related_name='sales',
        verbose_name=_('Cliente')
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha'))
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Subtotal')
    )
    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_('Descuento')
    )
    tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_('Impuesto')
    )
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Tasa de Impuesto')
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Total')
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
        verbose_name=_('Método de Pago')
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_('Estado')
    )
    notes = models.TextField(blank=True, verbose_name=_('Observaciones'))
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        related_name='sales_created',
        verbose_name=_('Creado por')
    )
    shift_number = models.PositiveIntegerField(default=1, verbose_name=_('Número de turno'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sales'
        ordering = ['-date']
        verbose_name = _('Venta')
        verbose_name_plural = _('Ventas')
    
    def __str__(self):
        return f"{self.invoice_number} - {self.client.name}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)
    
    def generate_invoice_number(self):
        """Generar número de factura secuencial"""
        from django.utils import timezone
        year = timezone.now().strftime('%Y')
        month = timezone.now().strftime('%m')
        last_sale = Sale.objects.filter(
            created_at__year=timezone.now().year,
            created_at__month=timezone.now().month
        ).order_by('-created_at').first()
        
        if last_sale:
            number = int(last_sale.invoice_number.split('-')[-1]) + 1
        else:
            number = 1
        
        return f"FAC-{year}{month}-{str(number).zfill(4)}"
    
    def calculate_totals(self):
        """Calcular subtotal, impuesto y total"""
        self.subtotal = sum(detail.total for detail in self.details.all())
        self.tax = self.subtotal * (self.tax_rate / 100)
        self.total = self.subtotal + self.tax - self.discount
        return self.total

class SaleDetail(models.Model):
    """Modelo de detalles de venta"""
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='details',
        verbose_name=_('Venta')
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='sale_details',
        verbose_name=_('Producto')
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_('Cantidad')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Precio Unitario')
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_('Descuento')
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Total')
    )
    
    class Meta:
        db_table = 'sale_details'
        verbose_name = _('Detalle de Venta')
        verbose_name_plural = _('Detalles de Venta')
    
    def __str__(self):
        return f"{self.sale.invoice_number} - {self.product.name}"
    
    def save(self, *args, **kwargs):
        self.total = (self.price * self.quantity) - self.discount
        super().save(*args, **kwargs)