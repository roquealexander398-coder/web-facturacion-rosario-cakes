from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

class Client(models.Model):
    """Modelo de clientes"""
    
    class Types(models.TextChoices):
        PERSON = 'PERSON', _('Persona Física')
        COMPANY = 'COMPANY', _('Empresa')
    
    name = models.CharField(max_length=200, verbose_name=_('Nombre/Razón Social'))
    client_type = models.CharField(
        max_length=10,
        choices=Types.choices,
        default=Types.PERSON,
        verbose_name=_('Tipo de Cliente')
    )
    identification = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name=_('Identificación (Cédula/RNC)')
    )
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    phone = models.CharField(max_length=20, verbose_name=_('Teléfono'))
    address = models.TextField(blank=True, verbose_name=_('Dirección'))
    is_active = models.BooleanField(default=True, verbose_name=_('Activo'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='clients_created'
    )
    
    class Meta:
        db_table = 'clients'
        ordering = ['-created_at']
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')
    
    def __str__(self):
        return f"{self.name} - {self.identification}"