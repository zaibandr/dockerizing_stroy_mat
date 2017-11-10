import django_tables2 as tables

from .models import Shipment


class ShipmentTable(tables.Table):
    class Meta:
        model = Shipment
        fields = (
            'product',
            'customer',
            'provider',
            'transporter',
            'address',

            'description',

            'volume',
            'cost_in',
            'cost_out',

            'stamp',
            'confidant',

            'price_delivery',


            'price_total',
            'profit',
        )