from django import forms

from .models import Provider, ProviderProduct


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = (
            'name', 'provider_type', 'rnc', 'email', 'phone', 'address',
            'contact_person', 'contact_phone', 'website', 'notes', 'is_active'
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'provider_type': forms.Select(attrs={'class': 'form-select'}),
            'rnc': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProviderProductForm(forms.ModelForm):
    class Meta:
        model = ProviderProduct
        fields = ('product', 'provider_code', 'price', 'delivery_time', 'is_preferred')
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'provider_code': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'delivery_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_preferred': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
