from django.contrib import admin

from .models import Provider, ProviderProduct


class ProviderProductInline(admin.TabularInline):
    model = ProviderProduct
    extra = 0


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'rnc', 'provider_type', 'phone', 'is_active')
    list_filter = ('provider_type', 'is_active')
    search_fields = ('name', 'rnc')
    inlines = [ProviderProductInline]


@admin.register(ProviderProduct)
class ProviderProductAdmin(admin.ModelAdmin):
    list_display = ('provider', 'product', 'price', 'is_preferred')
