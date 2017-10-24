from django.contrib import admin
from haystack.admin import SearchModelAdmin
from .models import Provider, Product
from leaflet.admin import LeafletGeoAdminMixin
# Register your models here.


def make_hidden(modeladmin, request, queryset):
    queryset.update(hidden=True)

make_hidden.short_description = "Не показывать отмеченных поставщиков"


def make_unhidden(modeladmin, request, queryset):
    queryset.update(hidden=False)

make_unhidden.short_description = "Показывать отмеченных поставщиков"


class CustomLeafletGeoAdminMixin(LeafletGeoAdminMixin):
    map_height = '800px'


class ProviderAdmin(CustomLeafletGeoAdminMixin, SearchModelAdmin):
    list_display = ('name', 'pk', 'contact_name', 'balance', 'orders_count', 'hidden')
    list_filter = ('hidden',)
    search_fields = ('pk', 'name', 'contact_name')
    actions = [make_hidden, make_unhidden]


class ProductAdmin(SearchModelAdmin):
    list_display = ('name',)
    # list_filter = ('manager')
    search_fields = ('name',)


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Product, ProductAdmin)
