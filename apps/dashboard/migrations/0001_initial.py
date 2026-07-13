# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='DashboardWidget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('widget_type', models.CharField(choices=[('CHART', 'Gráfico'), ('STATS', 'Estadísticas'), ('TABLE', 'Tabla'), ('CALENDAR', 'Calendario'), ('ACTIVITY', 'Actividad Reciente')], max_length=20, verbose_name='Tipo')),
                ('config', models.JSONField(default=dict, verbose_name='Configuración')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='Posición')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Widget',
                'verbose_name_plural': 'Widgets',
                'db_table': 'dashboard_widgets',
                'ordering': ['position'],
            },
        ),
    ]
