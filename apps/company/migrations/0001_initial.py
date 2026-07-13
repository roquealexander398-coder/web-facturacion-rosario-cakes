from django.db import migrations, models
import django.db.models.deletion
import django.core.validators

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(default='Mi Empresa', max_length=200, verbose_name='Nombre de la Empresa')),
                ('commercial_name', models.CharField(blank=True, max_length=200, verbose_name='Nombre Comercial')),
                ('rnc', models.CharField(default='123456789', max_length=20, verbose_name='RNC')),
                ('phone', models.CharField(default='809-555-5555', max_length=20, verbose_name='Teléfono')),
                ('email', models.EmailField(default='info@miempresa.com', max_length=254, verbose_name='Email')),
                ('website', models.URLField(blank=True, verbose_name='Sitio Web')),
                ('address', models.TextField(default='Calle Principal #123, Santo Domingo', verbose_name='Dirección')),
                ('city', models.CharField(default='Santo Domingo', max_length=100, verbose_name='Ciudad')),
                ('country', models.CharField(default='República Dominicana', max_length=100, verbose_name='País')),
                ('tax_rate', models.DecimalField(decimal_places=2, default=18.0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Tasa de Impuesto (%)')),
                ('currency', models.CharField(default='DOP', max_length=10, verbose_name='Moneda')),
                ('currency_symbol', models.CharField(default='RD$', max_length=5, verbose_name='Símbolo de Moneda')),
                ('invoice_prefix', models.CharField(default='FAC', max_length=10, verbose_name='Prefijo de Factura')),
                ('invoice_sequence_start', models.PositiveIntegerField(default=1, verbose_name='Inicio de Secuencia')),
                ('next_invoice_number', models.PositiveIntegerField(default=1, verbose_name='Próximo Número de Factura')),
                ('report_logo', models.ImageField(blank=True, null=True, upload_to='company/', verbose_name='Logo para Reportes')),
                ('footer_text', models.TextField(blank=True, verbose_name='Texto de Pie de Página')),
                ('timezone', models.CharField(default='America/Santo_Domingo', max_length=50, verbose_name='Zona Horaria')),
                ('date_format', models.CharField(default='%d/%m/%Y', max_length=20, verbose_name='Formato de Fecha')),
                ('time_format', models.CharField(default='%H:%M', max_length=20, verbose_name='Formato de Hora')),
                ('low_stock_alert_email', models.EmailField(blank=True, max_length=254, verbose_name='Email para Alertas de Stock')),
                ('low_stock_threshold', models.PositiveIntegerField(default=5, verbose_name='Umbral de Stock Bajo')),
                ('api_key', models.CharField(blank=True, max_length=255, verbose_name='API Key')),
                ('webhook_url', models.URLField(blank=True, verbose_name='Webhook URL')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_updates', to='accounts.user')),
            ],
            options={
                'db_table': 'company_config',
                'verbose_name': 'Configuración de Empresa',
                'verbose_name_plural': 'Configuración de Empresa',
            },
        ),
    ]