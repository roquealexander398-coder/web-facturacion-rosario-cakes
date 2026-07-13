@echo off
REM Script para preparar el proyecto para producción en Render
REM Este script debe ejecutarse en Windows antes de desplegar

echo ========================================
echo Sistema de Facturacion - Setup Produccion
echo ========================================

REM 1. Instalar dependencias
echo.
echo [1/4] Instalando dependencias...
.venv\Scripts\pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)

REM 2. Recolectar archivos estáticos
echo.
echo [2/4] Recolectando archivos estaticos...
.venv\Scripts\python manage.py collectstatic --noinput --clear
if errorlevel 1 (
    echo Error collecting static files
    pause
    exit /b 1
)

REM 3. Ejecutar migraciones
echo.
echo [3/4] Ejecutando migraciones...
.venv\Scripts\python manage.py migrate
if errorlevel 1 (
    echo Error running migrations
    pause
    exit /b 1
)

REM 4. Probar con DEBUG=False
echo.
echo [4/4] Probando servidor con DEBUG=False...
echo.
echo Accede a: http://localhost:8000/login/
echo.
echo IMPORTANTE: Presiona Ctrl+C para detener el servidor cuando termines de probar.
echo.
pause

setlocal
set DEBUG=False
.venv\Scripts\python manage.py runserver 0.0.0.0:8000
