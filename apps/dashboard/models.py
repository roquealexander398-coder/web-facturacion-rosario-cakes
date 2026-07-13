from django.db import models
from django.utils.translation import gettext_lazy as _

class DashboardWidget(models.Model):
    """Modelo para widgets personalizables del dashboard"""
    
    class WidgetType(models.TextChoices):
        CHART = 'CHART', _('Gráfico')
        STATS = 'STATS', _('Estadísticas')
        TABLE = 'TABLE', _('Tabla')
        CALENDAR = 'CALENDAR', _('Calendario')
        ACTIVITY = 'ACTIVITY', _('Actividad Reciente')
    
    name = models.CharField(max_length=100, verbose_name=_('Nombre'))
    widget_type = models.CharField(max_length=20, choices=WidgetType.choices, verbose_name=_('Tipo'))
    config = models.JSONField(default=dict, verbose_name=_('Configuración'))
    position = models.PositiveIntegerField(default=0, verbose_name=_('Posición'))
    is_active = models.BooleanField(default=True, verbose_name=_('Activo'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'dashboard_widgets'
        ordering = ['position']
        verbose_name = _('Widget')
        verbose_name_plural = _('Widgets')
    
    def __str__(self):
        return self.name