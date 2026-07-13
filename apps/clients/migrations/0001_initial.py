from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre/Razón Social')),
                ('client_type', models.CharField(choices=[('PERSON', 'Persona Física'), ('COMPANY', 'Empresa')], default='PERSON', max_length=10, verbose_name='Tipo de Cliente')),
                ('identification', models.CharField(max_length=20, unique=True, verbose_name='Identificación (Cédula/RNC)')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, verbose_name='Teléfono')),
                ('address', models.TextField(blank=True, verbose_name='Dirección')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients_created', to='accounts.user')),
            ],
            options={
                'db_table': 'clients',
                'ordering': ['-created_at'],
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
    ]