from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'clients'

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet)

urlpatterns = [
    path('', views.client_list, name='list'),
    path('crear/', views.client_create, name='create'),
    path('<int:pk>/', views.client_detail, name='detail'),
    path('<int:pk>/editar/', views.client_edit, name='edit'),
    path('<int:pk>/eliminar/', views.client_delete, name='delete'),
    path('api/', include(router.urls)),
]
