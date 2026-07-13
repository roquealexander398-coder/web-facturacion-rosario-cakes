from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'products'

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    path('', views.product_list, name='list'),
    path('crear/', views.product_create, name='create'),
    path('<int:pk>/', views.product_detail, name='detail'),
    path('<int:pk>/editar/', views.product_edit, name='edit'),
    path('<int:pk>/eliminar/', views.product_delete, name='delete'),
    path('api/', include(router.urls)),
]
