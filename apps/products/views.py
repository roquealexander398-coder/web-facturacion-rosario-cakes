from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from ..audit.models import AuditLog
from .forms import ProductForm
from .models import Product
from .serializers import ProductSerializer


@login_required
def product_list(request):
    products = Product.objects.all()
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(nombre__icontains=search) | Q(descripcion__icontains=search)
        )
    return render(request, 'products/list.html', {'products': products})


@login_required
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        product = form.save()
        return redirect('products:detail', pk=product.id_pastel)
    return render(request, 'products/form.html', {
        'form': form,
        'action': 'Crear',
    })


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product': product})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('products:detail', pk=product.id_pastel)
    return render(request, 'products/form.html', {
        'form': form,
        'action': 'Editar',
        'product': product,
    })


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products:list')
    return render(request, 'products/confirm_delete.html', {'product': product})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    filterset_fields = ['categoria', 'disponible']
    ordering_fields = ['nombre', 'precio_base']
    ordering = ['nombre']

    def perform_create(self, serializer):
        serializer.save()

