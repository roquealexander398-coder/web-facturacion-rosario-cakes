from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from ..audit.models import AuditLog
from .forms import ClientForm
from .models import Client
from .serializers import ClientSerializer


@login_required
def client_list(request):
    clients = Client.objects.all()
    search = request.GET.get('search')
    if search:
        clients = clients.filter(
            Q(nombre__icontains=search) | Q(email__icontains=search)
        )
    return render(request, 'clients/list.html', {'clients': clients})


@login_required
def client_create(request):
    form = ClientForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        client = form.save()
        AuditLog.objects.create(
            user=request.user,
            action='CREATE',
            model_name='Client',
            record_id=client.id_cliente,
            data_after={'nombre': client.nombre, 'email': client.email},
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
        )
        return redirect('clients:detail', pk=client.id_cliente)
    return render(request, 'clients/form.html', {'form': form, 'action': 'Crear'})


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'clients/detail.html', {'client': client})


@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('clients:detail', pk=client.id_cliente)
    return render(request, 'clients/form.html', {'form': form, 'action': 'Editar', 'client': client})


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('clients:list')
    return render(request, 'clients/confirm_delete.html', {'client': client})


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'email', 'telefono']
    filterset_fields = ['tipo_pago']
    ordering_fields = ['nombre', 'fecha_registro']
    ordering = ['nombre']

    def perform_create(self, serializer):
        serializer.save()

