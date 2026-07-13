from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.db import transaction
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Provider, ProviderProduct
from .serializers import ProviderSerializer, ProviderProductSerializer
from .forms import ProviderForm, ProviderProductForm
from ..audit.models import AuditLog

@login_required
def provider_list(request):
    """Vista para listar proveedores"""
    providers = Provider.objects.filter(is_active=True)
    return render(request, 'providers/list.html', {'providers': providers})

@login_required
def provider_create(request):
    """Vista para crear proveedor"""
    form = ProviderForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        provider = form.save(commit=False)
        provider.created_by = request.user
        provider.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='Provider',
            record_id=provider.id,
            data_after={'name': provider.name, 'rnc': provider.rnc},
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return redirect('providers:detail', pk=provider.id)
    
    return render(request, 'providers/form.html', {'form': form, 'action': 'Crear'})

@login_required
def provider_detail(request, pk):
    """Vista de detalle de proveedor"""
    provider = get_object_or_404(Provider, pk=pk)
    product_form = ProviderProductForm()
    provider_products = provider.products.select_related('product').all()
    
    return render(request, 'providers/detail.html', {
        'provider': provider,
        'product_form': product_form,
        'provider_products': provider_products
    })

@login_required
def provider_edit(request, pk):
    """Vista para editar proveedor"""
    provider = get_object_or_404(Provider, pk=pk)
    form = ProviderForm(request.POST or None, instance=provider)
    
    if request.method == 'POST' and form.is_valid():
        old_data = {
            'name': provider.name,
            'rnc': provider.rnc,
            'email': provider.email,
            'phone': provider.phone
        }
        provider = form.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Provider',
            record_id=provider.id,
            data_before=old_data,
            data_after={'name': provider.name, 'rnc': provider.rnc, 'email': provider.email},
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return redirect('providers:detail', pk=provider.id)
    
    return render(request, 'providers/form.html', {'form': form, 'action': 'Editar', 'provider': provider})

@login_required
def provider_delete(request, pk):
    """Vista para eliminar proveedor (soft delete)"""
    provider = get_object_or_404(Provider, pk=pk)
    
    if request.method == 'POST':
        provider.is_active = False
        provider.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='DELETE',
            model_name='Provider',
            record_id=provider.id,
            data_before={'name': provider.name, 'rnc': provider.rnc},
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return redirect('providers:list')
    
    return render(request, 'providers/confirm_delete.html', {'provider': provider})

@login_required
def add_provider_product(request, provider_id):
    """Agregar producto a proveedor"""
    provider = get_object_or_404(Provider, pk=provider_id)
    
    if request.method == 'POST':
        form = ProviderProductForm(request.POST)
        if form.is_valid():
            provider_product = form.save(commit=False)
            provider_product.provider = provider
            provider_product.save()
            
            AuditLog.objects.create(
                user=request.user,
                action='CREATE',
                model_name='ProviderProduct',
                record_id=provider_product.id,
                data_after={'provider': provider.name, 'product': provider_product.product.name},
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
            
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid form'})

class ProviderViewSet(viewsets.ModelViewSet):
    """API ViewSet para proveedores"""
    queryset = Provider.objects.filter(is_active=True)
    serializer_class = ProviderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'rnc', 'email', 'phone']
    filterset_fields = ['provider_type', 'is_active']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def perform_create(self, serializer):
        provider = serializer.save(created_by=self.request.user)
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model_name='Provider',
            record_id=provider.id,
            data_after=serializer.data,
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT')
        )