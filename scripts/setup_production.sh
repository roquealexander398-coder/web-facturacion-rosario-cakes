#!/bin/bash

# Script de configuración para producción

echo "=== Configurando Sistema de Facturación para Producción ==="

# 1. Configurar variables de entorno
echo "Configurando variables de entorno..."
cp .env.example .env
echo "Por favor edita el archivo .env con tus configuraciones"

# 2. Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# 3. Crear base de datos
echo "Creando base de datos..."
python manage.py migrate

# 4. Crear superusuario
echo "Creando superusuario..."
python manage.py createsuperuser

# 5. Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# 6. Crear directorios necesarios
echo "Creando directorios necesarios..."
mkdir -p media/avatars
mkdir -p media/products
mkdir -p media/invoices
mkdir -p media/company
mkdir -p logs
mkdir -p staticfiles

# 7. Configurar permisos
echo "Configurando permisos..."
chmod -R 755 media/ logs/ staticfiles/

# 8. Configurar Gunicorn
echo "Configurando Gunicorn..."
cat > /etc/systemd/system/facturacion.service << EOF
[Unit]
Description=Facturacion Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/facturacion
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind unix:/var/www/facturacion/facturacion.sock facturacion.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# 9. Configurar NGINX
echo "Configurando NGINX..."
cat > /etc/nginx/sites-available/facturacion << EOF
server {
    listen 80;
    server_name facturacion.com;
    
    location /static/ {
        alias /var/www/facturacion/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/facturacion/media/;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/facturacion/facturacion.sock;
    }
}
EOF

# 10. Habilitar sitio
ln -s /etc/nginx/sites-available/facturacion /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx

# 11. Configurar SSL con Let's Encrypt
echo "Configurando SSL..."
certbot --nginx -d facturacion.com

echo "=== Configuración completada ==="
echo "El sistema está listo para producción"