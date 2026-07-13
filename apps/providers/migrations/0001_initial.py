from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre/Razón Social')),
                ('provider_type', models.CharField(choices=[('NATIONAL', 'Nacional'), ('INTERNATIONAL', 'Internacional')], default='NATIONAL', max_length=20, verbose_name='Tipo')),
                ('rnc', models.CharField(max_length=20, unique=True, verbose_name='RNC')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, verbose_name='Teléfono')),
                ('address', models.TextField(blank=True, verbose_name='Dirección')),
                ('contact_person', models.CharField(blank=True, max_length=100, verbose_name='Persona de Contacto')),
                ('contact_phone', models.CharField(blank=True, max_length=20, verbose_name='Teléfono de Contacto')),
                ('website', models.URLField(blank=True, verbose_name='Sitio Web')),
                ('notes', models.TextField(blank=True, verbose_name='Observaciones')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='providers_created', to='accounts.user')),
            ],
            options={
                'db_table': 'providers',
                'ordering': ['name'],
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.CreateModel(
            name='ProviderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_code', models.CharField(blank=True, max_length=50, verbose_name='Código del Proveedor')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
                ('delivery_time', models.PositiveIntegerField(default=1, verbose_name='Tiempo de Entrega (días)')),
                ('is_preferred', models.BooleanField(default=False, verbose_name='Proveedor Preferido')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='providers', to='products.product', verbose_name='Producto')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='providers.provider', verbose_name='Proveedor')),
            ],
            options={
                'db_table': 'provider_products',
                'verbose_name': 'Producto por Proveedor',
                'verbose_name_plural': 'Productos por Proveedor',
                'unique_together': {('provider', 'product')},
            },
        ),
    ]