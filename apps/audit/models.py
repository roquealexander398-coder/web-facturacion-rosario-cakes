from django.db import models
from django.utils.translation import gettext_lazy as _

class AuditLog(models.Model):
    """Modelo de registro de auditoría"""
    
    class Action(models.TextChoices):
        CREATE = 'CREATE', _('Creación')
        UPDATE = 'UPDATE', _('Actualización')
        DELETE = 'DELETE', _('Eliminación')
        LOGIN = 'LOGIN', _('Inicio de Sesión')
        LOGOUT = 'LOGOUT', _('Cierre de Sesión')
        VIEW = 'VIEW', _('Visualización')
        EXPORT = 'EXPORT', _('Exportación')
        PRINT = 'PRINT', _('Impresión')
    
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        verbose_name=_('Usuario')
    )
    action = models.CharField(
        max_length=10,
        choices=Action.choices,
        verbose_name=_('Acción')
    )
    model_name = models.CharField(max_length=100, verbose_name=_('Modelo'))
    record_id = models.PositiveIntegerField(verbose_name=_('ID del Registro'))
    data_before = models.JSONField(blank=True, null=True, verbose_name=_('Datos Anteriores'))
    data_after = models.JSONField(blank=True, null=True, verbose_name=_('Datos Nuevos'))
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_('Dirección IP'))
    user_agent = models.CharField(max_length=255, blank=True, verbose_name=_('User Agent'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha y Hora'))
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']
        verbose_name = _('Registro de Auditoría')
        verbose_name_plural = _('Registros de Auditoría')
    
    def __str__(self):
        username = self.user.username if self.user else 'Sistema'
        return f"{username} - {self.action} - {self.model_name}"