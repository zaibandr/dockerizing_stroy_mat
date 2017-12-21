from django.contrib import admin
from haystack.admin import SearchModelAdmin
from leaflet.admin import LeafletGeoAdminMixin

from .models import Product, Region, PickPoint
from provider_app.admin import RegionsInline, PickPointsInline


class CustomLeafletGeoAdminMixin(LeafletGeoAdminMixin):
    map_height = '800px'


class ProductAdmin(SearchModelAdmin):
    list_display = ('name',)
    # list_filter = ('manager')
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)


class RegionAdmin(CustomLeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ('pk', 'description', )
    filter_horizontal = ('products', )

    # inlines = [
    #     RegionsInline,
    #     PickPointsInline
    # ]

admin.site.register(Region, RegionAdmin)


class PickPointAdmin(CustomLeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ('pk', 'description', )
    filter_horizontal = ('products',)

    # inlines = [
    #     RegionsInline,
    #     PickPointsInline
    # ]

admin.site.register(PickPoint, PickPointAdmin)