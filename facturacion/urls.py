from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Sistema de Facturación API",
        default_version='v1',
        description="API para sistema de facturación profesional",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@facturacion.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', lambda request: redirect('accounts:login', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Apps URLs
    path('', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('clientes/', include('apps.clients.urls')),
    path('proveedores/', include('apps.providers.urls')),
    path('productos/', include('apps.products.urls')),
    path('ventas/', include('apps.sales.urls')),
    path('auditoria/', include('apps.audit.urls')),
    path('configuracion/', include('apps.company.urls')),
    
    # API URLs
    path('api/', include('apps.dashboard.api_urls')),
    path('api/', include('apps.accounts.api_urls')),
    path('api/', include('apps.clients.api_urls')),
    path('api/', include('apps.products.api_urls')),
    path('api/', include('apps.sales.api_urls')),
    path('api/', include('apps.audit.api_urls')),
    path('api/', include('apps.company.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass