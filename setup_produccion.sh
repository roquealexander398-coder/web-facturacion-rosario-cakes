#!/bin/bash

# Script para preparar el proyecto para producción en Render
# Este script debe ejecutarse en Linux/Mac antes de desplegar

echo "========================================"
echo "Sistema de Facturacion - Setup Produccion"
echo "========================================"

# 1. Instalar dependencias
echo ""
echo "[1/4] Instalando dependencias..."
source .venv/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing dependencies"
    exit 1
fi

# 2. Recolectar archivos estáticos
echo ""
echo "[2/4] Recolectando archivos estaticos..."
python manage.py collectstatic --noinput --clear
if [ $? -ne 0 ]; then
    echo "Error collecting static files"
    exit 1
fi

# 3. Ejecutar migraciones
echo ""
echo "[3/4] Ejecutando migraciones..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error running migrations"
    exit 1
fi

# 4. Probar con DEBUG=False
echo ""
echo "[4/4] Probando servidor con DEBUG=False..."
echo ""
echo "Accede a: http://localhost:8000/login/"
echo ""
echo "IMPORTANTE: Presiona Ctrl+C para detener el servidor cuando termines de probar."
echo ""

export DEBUG=False
python manage.py runserver 0.0.0.0:8000
