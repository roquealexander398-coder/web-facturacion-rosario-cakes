from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.db import transaction
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CompanyConfig
from .forms import CompanyConfigForm
from ..audit.models import AuditLog

@login_required
@permission_required('company.can_manage_company', raise_exception=True)
def company_config(request):
    """Vista de configuración de empresa"""
    config = CompanyConfig.get_config()
    form = CompanyConfigForm(request.POST or None, request.FILES or None, instance=config)
    
    if request.method == 'POST' and form.is_valid():
        old_data = {
            'company_name': config.company_name,
            'rnc': config.rnc,
            'email': config.email,
            'phone': config.phone,
            'tax_rate': config.tax_rate
        }
        
        config = form.save(commit=False)
        config.updated_by = request.user
        config.save()
        
        # Si se subió un logo, procesarlo
        if 'report_logo' in request.FILES:
            config.report_logo = request.FILES['report_logo']
            config.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='CompanyConfig',
            record_id=config.id,
            data_before=old_data,
            data_after={
                'company_name': config.company_name,
                'rnc': config.rnc,
                'email': config.email,
                'phone': config.phone,
                'tax_rate': float(config.tax_rate)
            },
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return redirect('company:config')
    
    return render(request, 'company/config.html', {
        'form': form,
        'config': config
    })

@login_required
def reset_invoice_sequence(request):
    """Resetear la secuencia de facturación"""
    if request.method == 'POST':
        config = CompanyConfig.get_config()
        config.next_invoice_number = config.invoice_sequence_start
        config.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='CompanyConfig',
            record_id=config.id,
            data_after={'next_invoice_number': config.next_invoice_number},
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Secuencia de facturación reiniciada exitosamente'
        })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

class CompanyConfigViewSet(viewsets.ViewSet):
    """API para configuración de empresa"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def info(self, request):
        """Obtener información de la empresa"""
        config = CompanyConfig.get_config()
        return Response({
            'company_name': config.company_name,
            'commercial_name': config.commercial_name,
            'rnc': config.rnc,
            'phone': config.phone,
            'email': config.email,
            'address': config.address,
            'tax_rate': float(config.tax_rate),
            'currency_symbol': config.currency_symbol,
            'currency': config.currency,
            'logo_url': config.report_logo.url if config.report_logo else None
        })