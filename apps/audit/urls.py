from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'audit'

router = DefaultRouter()
router.register(r'audit', views.AuditLogViewSet)

urlpatterns = [
    path('', views.audit_logs, name='logs'),
    path('api/', include(router.urls)),
]
