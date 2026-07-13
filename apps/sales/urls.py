from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'sales'

router = DefaultRouter()
router.register(r'sales', views.SaleViewSet)

urlpatterns = [
    path('', views.sale_list, name='list'),
    path('crear/', views.sale_create, name='create'),
    path('cierre-turno/', views.shift_close, name='shift-close'),
    path('cierre-turno/imprimir/', views.shift_close_print, name='shift-close-print'),
    path('<int:pk>/', views.sale_detail, name='detail'),
    path('<int:pk>/eliminar/', views.sale_delete, name='delete'),
    path('<int:pk>/imprimir/', views.sale_receipt, name='receipt'),
    path('<int:pk>/pdf/', views.sale_print_pdf, name='pdf'),
    path('reportes/', views.sale_report, name='reports'),
    path('exportar/', views.export_sales_excel, name='export'),
    path('api/', include(router.urls)),
]
