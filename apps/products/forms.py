from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'nombre', 'descripcion', 'categoria',
            'precio_base', 'disponible', 'imagen'
        )
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'precio_base': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

