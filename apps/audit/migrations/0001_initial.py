from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('CREATE', 'Creación'), ('UPDATE', 'Actualización'), ('DELETE', 'Eliminación'), ('LOGIN', 'Inicio de Sesión'), ('LOGOUT', 'Cierre de Sesión'), ('VIEW', 'Visualización'), ('EXPORT', 'Exportación'), ('PRINT', 'Impresión')], max_length=10, verbose_name='Acción')),
                ('model_name', models.CharField(max_length=100, verbose_name='Modelo')),
                ('record_id', models.PositiveIntegerField(verbose_name='ID del Registro')),
                ('data_before', models.JSONField(blank=True, null=True, verbose_name='Datos Anteriores')),
                ('data_after', models.JSONField(blank=True, null=True, verbose_name='Datos Nuevos')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='Dirección IP')),
                ('user_agent', models.CharField(blank=True, max_length=255, verbose_name='User Agent')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audit_logs', to='accounts.user', verbose_name='Usuario')),
            ],
            options={
                'db_table': 'audit_logs',
                'ordering': ['-created_at'],
                'verbose_name': 'Registro de Auditoría',
                'verbose_name_plural': 'Registros de Auditoría',
            },
        ),
    ]