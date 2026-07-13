from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'providers'

router = DefaultRouter()
router.register(r'providers', views.ProviderViewSet)

urlpatterns = [
    path('', views.provider_list, name='list'),
    path('crear/', views.provider_create, name='create'),
    path('<int:pk>/', views.provider_detail, name='detail'),
    path('<int:pk>/editar/', views.provider_edit, name='edit'),
    path('<int:pk>/eliminar/', views.provider_delete, name='delete'),
    path('<int:provider_id>/agregar-producto/', views.add_provider_product, name='add_product'),
    path('api/', include(router.urls)),
]