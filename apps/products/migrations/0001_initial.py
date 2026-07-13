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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activa')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='products.category', verbose_name='Categoría Padre')),
            ],
            options={
                'db_table': 'categories',
                'ordering': ['name'],
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Código')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('unit', models.CharField(choices=[('UNIT', 'Unidad'), ('KG', 'Kilogramo'), ('LB', 'Libra'), ('L', 'Litro'), ('ML', 'Mililitro'), ('M', 'Metro'), ('CM', 'Centímetro')], default='UNIT', max_length=10, verbose_name='Unidad de Medida')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Precio de Venta')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Costo')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stock Actual')),
                ('min_stock', models.PositiveIntegerField(default=5, verbose_name='Stock Mínimo')),
                ('max_stock', models.PositiveIntegerField(default=100, verbose_name='Stock Máximo')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Imagen')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category', verbose_name='Categoría')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products_created', to='accounts.user')),
            ],
            options={
                'db_table': 'products',
                'ordering': ['name'],
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='InventoryMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_type', models.CharField(choices=[('PURCHASE', 'Compra'), ('SALE', 'Venta'), ('RETURN', 'Devolución'), ('ADJUSTMENT', 'Ajuste'), ('TRANSFER', 'Transferencia')], max_length=10, verbose_name='Tipo de Movimiento')),
                ('quantity', models.PositiveIntegerField(verbose_name='Cantidad')),
                ('previous_stock', models.PositiveIntegerField(verbose_name='Stock Anterior')),
                ('new_stock', models.PositiveIntegerField(verbose_name='Nuevo Stock')),
                ('reference', models.CharField(blank=True, max_length=100, verbose_name='Referencia')),
                ('notes', models.TextField(blank=True, verbose_name='Observaciones')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventory_movements', to='accounts.user')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='products.product', verbose_name='Producto')),
            ],
            options={
                'db_table': 'inventory_movements',
                'ordering': ['-created_at'],
                'verbose_name': 'Movimiento de Inventario',
                'verbose_name_plural': 'Movimientos de Inventario',
            },
        ),
    ]