#!/bin/bash

# Script para gestión de base de datos

echo "=== Gestión de Base de Datos ==="
echo "1. Crear base de datos"
echo "2. Resetear base de datos (eliminar todo)"
echo "3. Crear backup"
echo "4. Restaurar backup"
echo "5. Verificar integridad"
echo "6. Salir"
echo "=============================="
read -p "Seleccione una opción: " option

case $option in
    1)
        echo "Creando base de datos..."
        python manage.py migrate
        python manage.py loaddata fixtures/initial_data.json
        echo "Base de datos creada exitosamente"
        ;;
    2)
        echo "ADVERTENCIA: Esto eliminará todos los datos"
        read -p "¿Está seguro? (s/N): " confirm
        if [ "$confirm" = "s" ] || [ "$confirm" = "S" ]; then
            python manage.py flush --noinput
            python manage.py migrate
            python manage.py loaddata fixtures/initial_data.json
            echo "Base de datos reseteada"
        else
            echo "Operación cancelada"
        fi
        ;;
    3)
        echo "Creando backup..."
        timestamp=$(date +%Y%m%d_%H%M%S)
        pg_dump -U postgres facturacion_db > backups/backup_$timestamp.sql
        echo "Backup creado: backups/backup_$timestamp.sql"
        ;;
    4)
        echo "Backups disponibles:"
        ls -la backups/*.sql 2>/dev/null || echo "No hay backups"
        read -p "Nombre del archivo: " filename
        if [ -f "backups/$filename" ]; then
            psql -U postgres -d facturacion_db < backups/$filename
            echo "Backup restaurado"
        else
            echo "Archivo no encontrado"
        fi
        ;;
    5)
        echo "Verificando integridad..."
        python manage.py check
        python manage.py showmigrations
        ;;
    6)
        echo "Saliendo..."
        exit 0
        ;;
    *)
        echo "Opción inválida"
        ;;
esac