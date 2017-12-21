import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html

from .models import Shipment


class ShipmentTableMixin(object):
    editlink = tables.Column(verbose_name='№ Отгрузки', empty_values=())

    provider = tables.Column(verbose_name='Поставщик')
    customer = tables.Column(verbose_name='Заказчик')

    price_delta = tables.Column(verbose_name='Прибыль за единицу', empty_values=())

    def render_editlink(self, record, value):
        if value is None:
            return format_html('<a href="{}"><p class="text-left">{}</p></a>',
                               reverse('shipment:shipment_edit', kwargs={'pk': record.pk}),
                               record.pk)
        else:
            return type(value)

    def render_price_delta(self, record, value):
        if value is None:
            return record.cost_out - record.cost_in
        else:
            return value

    def render_provider(self, record, value):
        return format_html('<a href="{}"><p class="text-left">{}</p></a>',
                           reverse('provider:provider_detail', kwargs={'pk': record.provider_id}),
                           value)

    def render_customer(self, record, value):
        return format_html('<a href="{}"><p class="text-left">{}</p></a>',
                           reverse('customer:customer_detail', kwargs={'pk': record.customer_id}),
                           value)


class ShipmentTable(ShipmentTableMixin, tables.Table):
    class Meta:
        model = Shipment
        fields = (
            'deliver', 'customer', 'address',
            'product', 'provider',

            'author',

            'transporter', 'price_delivery',

            'status',

            'volume_m', 'volume_s', 'volume_b',

            'cost_in', 'cost_out', 'stamp', 'confidant',

            'price_total',
            'profit',
            'created',
        )


class ManagerShipmentTable(ShipmentTableMixin, tables.Table):
    class Meta:
        model = Shipment
        fields = (
            'editlink',

            'deliver', 'customer', 'address',
            'product', 'volume_m',

            'provider',

            'transporter', 'price_delivery',

            'status',

            'cost_in', 'cost_out',

            'price_total',
            'profit',
            'price_delta',
            'created',
        )


class SupplierShipmentTable(ShipmentTableMixin, tables.Table):
    class Meta:
        model = Shipment
        fields = (
            'editlink',

            'deliver', 'customer', 'address',
            'product', 'volume_m', 'volume_s',

            'provider',

            'author',

            'transporter', 'price_delivery',

            'status',

            'cost_in', 'cost_out', 'stamp', 'confidant',

            'price_total',
            'profit',
            'price_delta',
            'created',
        )


class BookerShipmentTable(ShipmentTableMixin, tables.Table):
    class Meta:
        model = Shipment
        fields = (
            'editlink',

            'deliver', 'customer', 'address',
            'product',

            'volume_m', 'volume_s', 'volume_b',

            'provider',

            'author',

            'transporter', 'price_delivery',

            'status',

            'cost_in', 'cost_out', 'stamp', 'confidant',

            'price_total',
            'profit',
            'price_delta',
            'created',
        )
