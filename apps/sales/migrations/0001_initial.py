from django.db import migrations, models
import django.db.models.deletion
import django.core.validators

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('clients', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=20, unique=True, verbose_name='Número de Factura')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Subtotal')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Descuento')),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Impuesto')),
                ('tax_rate', models.DecimalField(decimal_places=2, default=18.0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Tasa de Impuesto')),
                ('total', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Total')),
                ('payment_method', models.CharField(choices=[('CASH', 'Efectivo'), ('CARD', 'Tarjeta'), ('TRANSFER', 'Transferencia'), ('CHECK', 'Cheque'), ('ONLINE', 'Pago en Línea')], default='CASH', max_length=10, verbose_name='Método de Pago')),
                ('status', models.CharField(choices=[('PENDING', 'Pendiente'), ('PAID', 'Pagada'), ('CANCELLED', 'Cancelada'), ('REFUNDED', 'Reembolsada')], default='PENDING', max_length=10, verbose_name='Estado')),
                ('notes', models.TextField(blank=True, verbose_name='Observaciones')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales', to='clients.client', verbose_name='Cliente')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales_created', to='accounts.user', verbose_name='Creado por')),
            ],
            options={
                'db_table': 'sales',
                'ordering': ['-date'],
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
            },
        ),
        migrations.CreateModel(
            name='SaleDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Cantidad')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Precio Unitario')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Descuento')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Total')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sale_details', to='products.product', verbose_name='Producto')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='sales.sale', verbose_name='Venta')),
            ],
            options={
                'db_table': 'sale_details',
                'verbose_name': 'Detalle de Venta',
                'verbose_name_plural': 'Detalles de Venta',
            },
        ),
    ]