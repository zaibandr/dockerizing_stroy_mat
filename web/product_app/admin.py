from django.contrib import admin
from haystack.admin import SearchModelAdmin
from leaflet.admin import LeafletGeoAdminMixin

from .models import Product, Region, PickPoint


class CustomLeafletGeoAdminMixin(LeafletGeoAdminMixin):
    map_height = '800px'


class ProductAdmin(SearchModelAdmin):
    list_display = ('name',)
    # list_filter = ('manager')
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)


class RegionAdmin(CustomLeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ('description', )

admin.site.register(Region, RegionAdmin)


class PickPointAdmin(CustomLeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ('description', )

admin.site.register(PickPoint, PickPointAdmin)