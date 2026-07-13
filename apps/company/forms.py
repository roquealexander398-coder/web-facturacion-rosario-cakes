from django import forms

from .models import CompanyConfig


class CompanyConfigForm(forms.ModelForm):
    class Meta:
        model = CompanyConfig
        fields = (
            'company_name', 'commercial_name', 'rnc', 'phone', 'email', 'website',
            'address', 'city', 'country', 'tax_rate', 'currency', 'currency_symbol',
            'invoice_prefix', 'invoice_sequence_start', 'report_logo', 'footer_text',
            'timezone', 'date_format', 'time_format',
            'low_stock_alert_email', 'low_stock_threshold', 'api_key', 'webhook_url',
        )
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'commercial_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rnc': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'currency_symbol': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_prefix': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_sequence_start': forms.NumberInput(attrs={'class': 'form-control'}),
            'report_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'footer_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'timezone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_format': forms.TextInput(attrs={'class': 'form-control'}),
            'time_format': forms.TextInput(attrs={'class': 'form-control'}),
            'low_stock_alert_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-control'}),
            'api_key': forms.TextInput(attrs={'class': 'form-control'}),
            'webhook_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
