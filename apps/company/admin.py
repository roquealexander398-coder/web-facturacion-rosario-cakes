from django.contrib import admin

from .models import CompanyConfig


@admin.register(CompanyConfig)
class CompanyConfigAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'rnc', 'tax_rate', 'updated_at')
