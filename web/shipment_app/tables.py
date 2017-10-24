import django_tables2 as tables
from .models import Shipment


class ShipmentTable(tables.Table):
    class Meta:
        model = Shipment
        fields = (
            'product',
            # 'status',
            'customer',
            'provider',
            'transporter',
            'address',
            'volume',

            'cost_in',
            'cost_out',
            'price',
            'profit',
        )