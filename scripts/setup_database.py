#!/usr/bin/env python
"""
Script para configurar la base de datos desde cero
Ejecutar: python scripts/setup_database.py
"""

import os
import sys
import django
from django.core.management import call_command
from django.db import connection

# Configurar entorno Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facturacion.settings')
django.setup()

def setup_database():
    """Configurar base de datos completa"""
    
    print("=== Configuración de Base de Datos ===\n")
    
    # 1. Crear base de datos si no existe (PostgreSQL)
    print("1. Verificando base de datos...")
    db_name = os.getenv('DB_NAME', 'facturacion_db')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", [db_name])
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creando base de datos: {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name}")
        else:
            print(f"Base de datos {db_name} ya existe")
    
    # 2. Ejecutar migraciones
    print("\n2. Ejecutando migraciones...")
    call_command('makemigrations')
    call_command('migrate')
    
    # 3. Crear superusuario
    print("\n3. Creando superusuario...")
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@facturacion.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema',
            role='ADMIN'
        )
        print("Superusuario creado: admin / admin123")
    else:
        print("Superusuario ya existe")
    
    # 4. Cargar datos iniciales
    print("\n4. Cargando datos iniciales...")
    try:
        call_command('loaddata', 'fixtures/initial_data.json')
        print("Datos iniciales cargados exitosamente")
    except Exception as e:
        print(f"Error al cargar datos: {e}")
    
    # 5. Verificar instalación
    print("\n5. Verificando instalación...")
    from apps.company.models import CompanyConfig
    
    try:
        config = CompanyConfig.get_config()
        print(f"Configuración de empresa: {config.company_name}")
        print(f"Moneda: {config.currency_symbol}")
        print(f"Tasa de impuesto: {config.tax_rate}%")
    except Exception as e:
        print(f"Error al verificar configuración: {e}")
    
    # 6. Estadísticas
    print("\n=== Estadísticas de la Base de Datos ===")
    
    from apps.clients.models import Client
    from apps.products.models import Product, Category
    from apps.providers.models import Provider
    from apps.sales.models import Sale
    
    print(f"Usuarios: {User.objects.count()}")
    print(f"Clientes: {Client.objects.count()}")
    print(f"Proveedores: {Provider.objects.count()}")
    print(f"Categorías: {Category.objects.count()}")
    print(f"Productos: {Product.objects.count()}")
    print(f"Ventas: {Sale.objects.count()}")
    
    print("\n=== Configuración completada exitosamente! ===")
    print("Puedes iniciar el servidor con: python manage.py runserver")
    print("Accede al sistema con:")
    print("  Usuario: admin")
    print("  Contraseña: admin123")

if __name__ == '__main__':
    try:
        setup_database()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)