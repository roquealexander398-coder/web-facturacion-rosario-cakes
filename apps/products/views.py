from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from ..audit.models import AuditLog
from .forms import ProductForm
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


@login_required
def product_list(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(code__icontains=search)
        )
    return render(request, 'products/list.html', {'products': products})


@login_required
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.created_by = request.user
        product.save()
        return redirect('products:detail', pk=product.id)
    return render(request, 'products/form.html', {
        'form': form,
        'action': 'Crear',
        'categories': Category.objects.filter(is_active=True),
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
        return redirect('products:detail', pk=product.id)
    return render(request, 'products/form.html', {
        'form': form,
        'action': 'Editar',
        'product': product,
        'categories': Category.objects.filter(is_active=True),
    })


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_active = False
        product.save()
        return redirect('products:list')
    return render(request, 'products/confirm_delete.html', {'product': product})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'name', 'description']
    filterset_fields = ['category', 'is_active', 'stock']
    ordering_fields = ['name', 'price', 'stock']
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        stock_gt = self.request.query_params.get('stock__gt')
        if stock_gt is not None:
            queryset = queryset.filter(stock__gt=int(stock_gt))
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    ordering = ['name']
