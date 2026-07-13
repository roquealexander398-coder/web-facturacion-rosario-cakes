import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facturacion.settings')

application = get_wsgi_application()

# Servir archivos estáticos con WhiteNoise (para producción en Render)
if os.getenv('DEBUG', 'True') == 'False':
    application = WhiteNoise(application, root=os.path.join(os.path.dirname(__file__), '..', 'staticfiles'))
