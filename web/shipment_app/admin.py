from django.contrib import admin

from .models import Shipment


class ShipmentAdmin(admin.ModelAdmin):
    fields = (
        'product', 'author', 'volume_m', 'volume_s', 'volume_b',
        'customer', 'provider', 'transporter',
        'status', 'stamp', 'confidant', 'cost_in', 'cost_out',
        'price_delivery', 'deliver', 'confirmed',

    )
    list_display = (
        'id', 'product', 'volume_m', 'customer', 'provider',
        'status', 'stamp', 'cost_in', 'cost_out',)
    list_filter = ('status', 'product__name', 'customer__name', 'provider__name')

    # def get_product(self, obj):
    #     return obj.product.name
    #
    # def get_customer(self, obj):
    #     return obj.customer.name
    #
    # def get_provider(self, obj):
    #     return obj.provider.name
    #
    # get_product.admin_order_field = 'product__name'
    # get_customer.admin_order_field = 'customer__name'
    # get_provider.admin_order_field= 'provider__name'

    # search_fields = ('pk', 'name', 'contact_name')

admin.site.register(Shipment, ShipmentAdmin)