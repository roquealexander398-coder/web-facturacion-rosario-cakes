from django.db import models
from django.utils.translation import gettext_lazy as _

class Provider(models.Model):
    """Modelo de proveedores"""
    
    class Types(models.TextChoices):
        NATIONAL = 'NATIONAL', _('Nacional')
        INTERNATIONAL = 'INTERNATIONAL', _('Internacional')
    
    name = models.CharField(max_length=200, verbose_name=_('Nombre/Razón Social'))
    provider_type = models.CharField(
        max_length=20,
        choices=Types.choices,
        default=Types.NATIONAL,
        verbose_name=_('Tipo')
    )
    rnc = models.CharField(max_length=20, unique=True, verbose_name=_('RNC'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    phone = models.CharField(max_length=20, verbose_name=_('Teléfono'))
    address = models.TextField(blank=True, verbose_name=_('Dirección'))
    contact_person = models.CharField(max_length=100, blank=True, verbose_name=_('Persona de Contacto'))
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name=_('Teléfono de Contacto'))
    website = models.URLField(blank=True, verbose_name=_('Sitio Web'))
    notes = models.TextField(blank=True, verbose_name=_('Observaciones'))
    is_active = models.BooleanField(default=True, verbose_name=_('Activo'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='providers_created'
    )
    
    class Meta:
        db_table = 'providers'
        ordering = ['name']
        verbose_name = _('Proveedor')
        verbose_name_plural = _('Proveedores')
    
    def __str__(self):
        return f"{self.name} - {self.rnc}"

class ProviderProduct(models.Model):
    """Modelo de productos por proveedor"""
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('Proveedor')
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='providers',
        verbose_name=_('Producto')
    )
    provider_code = models.CharField(max_length=50, blank=True, verbose_name=_('Código del Proveedor'))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Precio')
    )
    delivery_time = models.PositiveIntegerField(default=1, verbose_name=_('Tiempo de Entrega (días)'))
    is_preferred = models.BooleanField(default=False, verbose_name=_('Proveedor Preferido'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'provider_products'
        unique_together = ['provider', 'product']
        verbose_name = _('Producto por Proveedor')
        verbose_name_plural = _('Productos por Proveedor')
    
    def __str__(self):
        return f"{self.provider.name} - {self.product.name}"