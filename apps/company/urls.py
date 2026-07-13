from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'company'

router = DefaultRouter()
router.register(r'company', views.CompanyConfigViewSet, basename='company')

urlpatterns = [
    path('', views.company_config, name='config'),
    path('reset-sequence/', views.reset_invoice_sequence, name='reset_sequence'),
    path('api/', include(router.urls)),
]