from django.contrib import admin

from .models import Sale, SaleDetail


class SaleDetailInline(admin.TabularInline):
    model = SaleDetail
    extra = 0


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'client', 'total', 'status', 'date')
    list_filter = ('status', 'payment_method')
    search_fields = ('invoice_number', 'client__name')
    inlines = [SaleDetailInline]


@admin.register(SaleDetail)
class SaleDetailAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'total')
