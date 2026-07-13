from django import forms
from decimal import Decimal

from .models import Sale


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('client', 'payment_method', 'tax_rate', 'discount', 'notes', 'status')
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['discount'].required = False
        self.fields['status'].required = False

    def save(self, commit=True):
        sale = super().save(commit=False)
        if sale.subtotal is None:
            sale.subtotal = Decimal('0.00')
        if sale.tax is None:
            sale.tax = Decimal('0.00')
        if sale.total is None:
            sale.total = Decimal('0.00')
        if not sale.status:
            sale.status = Sale.Status.PENDING
        if commit:
            sale.save()
        return sale
