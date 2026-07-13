# Sistema de Facturación Rosario

Aplicación web de facturación desarrollada en Django.

## Requisitos
- Python 3.13+
- pip

## Instalación local
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Despliegue en Render
Este proyecto incluye:
- render.yaml
- build.sh

## Credenciales por defecto
- Usuario: admin
- Contraseña: admin123
