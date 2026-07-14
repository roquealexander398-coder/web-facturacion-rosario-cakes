from django import forms

from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            'nombre', 'tipo_pago', 'email',
            'telefono', 'direccion'
        )
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_pago': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

