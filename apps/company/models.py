from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class CompanyConfig(models.Model):
    """Modelo de configuración de la empresa"""
    
    # Información Básica
    company_name = models.CharField(max_length=200, default='ROSARIO CAKES', verbose_name=_('Nombre de la Empresa'))
    commercial_name = models.CharField(max_length=200, blank=True, verbose_name=_('Nombre Comercial'))
    rnc = models.CharField(max_length=20, default='123456789', verbose_name=_('RNC'))
    
    # Contacto
    phone = models.CharField(max_length=20, default='809-555-5555', verbose_name=_('Teléfono'))
    email = models.EmailField(default='info@miempresa.com', verbose_name=_('Email'))
    website = models.URLField(blank=True, verbose_name=_('Sitio Web'))
    
    # Dirección
    address = models.TextField(default='Calle Principal #123, Santo Domingo', verbose_name=_('Dirección'))
    city = models.CharField(max_length=100, default='Santo Domingo', verbose_name=_('Ciudad'))
    country = models.CharField(max_length=100, default='República Dominicana', verbose_name=_('País'))
    
    # Configuración Fiscal
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Tasa de Impuesto (%)')
    )
    currency = models.CharField(max_length=10, default='DOP', verbose_name=_('Moneda'))
    currency_symbol = models.CharField(max_length=5, default='RD$', verbose_name=_('Símbolo de Moneda'))
    
    # Configuración de Facturación
    invoice_prefix = models.CharField(max_length=10, default='FAC', verbose_name=_('Prefijo de Factura'))
    invoice_sequence_start = models.PositiveIntegerField(default=1, verbose_name=_('Inicio de Secuencia'))
    next_invoice_number = models.PositiveIntegerField(default=1, verbose_name=_('Próximo Número de Factura'))
    
    # Configuración de Reportes
    report_logo = models.ImageField(upload_to='company/', blank=True, null=True, verbose_name=_('Logo para Reportes'))
    footer_text = models.TextField(blank=True, verbose_name=_('Texto de Pie de Página'))
    
    # Configuración de Sistema
    timezone = models.CharField(max_length=50, default='America/Santo_Domingo', verbose_name=_('Zona Horaria'))
    date_format = models.CharField(max_length=20, default='%d/%m/%Y', verbose_name=_('Formato de Fecha'))
    time_format = models.CharField(max_length=20, default='%H:%M', verbose_name=_('Formato de Hora'))
    
    # Notificaciones
    low_stock_alert_email = models.EmailField(blank=True, verbose_name=_('Email para Alertas de Stock'))
    low_stock_threshold = models.PositiveIntegerField(default=5, verbose_name=_('Umbral de Stock Bajo'))
    
    # Integraciones
    api_key = models.CharField(max_length=255, blank=True, verbose_name=_('API Key'))
    webhook_url = models.URLField(blank=True, verbose_name=_('Webhook URL'))
    
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='company_updates'
    )
    
    class Meta:
        db_table = 'company_config'
        verbose_name = _('Configuración de Empresa')
        verbose_name_plural = _('Configuración de Empresa')
        permissions = [
            ('can_manage_company', 'Puede gestionar la configuración de empresa'),
        ]
    
    def __str__(self):
        return self.company_name
    
    @classmethod
    def get_config(cls):
        """Obtener la configuración de la empresa (singleton)"""
        config, created = cls.objects.get_or_create(
            id=1,
            defaults={
                'company_name': 'ROSARIO CAKES',
                'rnc': '123456789',
                'phone': '809-555-5555',
                'email': 'info@miempresa.com',
                'address': 'Calle Principal #123, Santo Domingo'
            }
        )
        return config
    
    def get_next_invoice_number(self):
        """Obtener el siguiente número de factura"""
        current = self.next_invoice_number
        self.next_invoice_number += 1
        self.save()
        return current
    
    def format_currency(self, amount):
        """Formatear monto con símbolo de moneda"""
        return f"{self.currency_symbol} {amount:,.2f}"