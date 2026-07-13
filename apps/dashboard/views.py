from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from ..sales.models import Sale
from ..products.models import Product
from ..clients.models import Client
from ..audit.models import AuditLog

@login_required
def dashboard_index(request):
    """Vista principal del dashboard"""
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    current_shift = int(request.session.get('sales_current_shift', 1))
    
    # Estadísticas del día
    today_sales = Sale.objects.filter(date__date=today, shift_number=current_shift)
    today_total = today_sales.aggregate(total=Sum('total'))['total'] or 0
    today_count = today_sales.count()
    
    # Estadísticas de la semana
    week_sales = Sale.objects.filter(date__date__gte=start_of_week, shift_number=current_shift)
    week_total = week_sales.aggregate(total=Sum('total'))['total'] or 0
    
    # Estadísticas del mes
    month_sales = Sale.objects.filter(date__date__gte=start_of_month, shift_number=current_shift)
    month_total = month_sales.aggregate(total=Sum('total'))['total'] or 0
    
    # Productos con bajo stock
    low_stock_products = Product.objects.filter(stock__lte=F('min_stock'), is_active=True)[:10]
    
    # Clientes recientes
    recent_clients = Client.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # Ventas recientes
    recent_sales = Sale.objects.filter(shift_number=current_shift).select_related('client', 'created_by').order_by('-date')[:10]
    
    # Actividad reciente
    recent_activity = AuditLog.objects.select_related('user').order_by('-created_at')[:10]
    
    context = {
        'today_total': today_total,
        'today_count': today_count,
        'week_total': week_total,
        'month_total': month_total,
        'low_stock_products': low_stock_products,
        'recent_clients': recent_clients,
        'recent_sales': recent_sales,
        'recent_activity': recent_activity,
        'client_count': Client.objects.filter(is_active=True).count(),
        'product_count': Product.objects.filter(is_active=True).count(),
        'total_sales': Sale.objects.filter(shift_number=current_shift).count(),
    }
    
    return render(request, 'dashboard/index.html', context)

class DashboardStatsViewSet(viewsets.ViewSet):
    """API para estadísticas del dashboard"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def sales_chart(self, request):
        """Obtener datos para gráfico de ventas"""
        days = int(request.query_params.get('days', 30))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        sales_data = []
        for i in range(days):
            date = start_date + timedelta(days=i)
            daily_total = Sale.objects.filter(
                date__date=date,
                status='PAID'
            ).aggregate(total=Sum('total'))['total'] or 0
            
            sales_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'total': float(daily_total)
            })
        
        return Response(sales_data)
    
    @action(detail=False, methods=['get'])
    def top_products(self, request):
        """Obtener productos más vendidos"""
        from django.db.models import Sum
        
        top_products = Sale.objects.filter(
            status='PAID'
        ).values(
            'details__product__name'
        ).annotate(
            total_sold=Sum('details__quantity')
        ).order_by('-total_sold')[:10]
        
        return Response(top_products)
    
    @action(detail=False, methods=['get'])
    def sales_by_hour(self, request):
        """Obtener ventas por hora del día"""
        from django.db.models import Count
        
        hourly_sales = Sale.objects.filter(
            date__date=timezone.now().date()
        ).extra(
            select={'hour': "EXTRACT(hour FROM date)"}
        ).values('hour').annotate(
            count=Count('id')
        ).order_by('hour')
        
        return Response(hourly_sales)