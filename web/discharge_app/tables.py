import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html

from .models import DischargeEntity, DischargeProvider, DischargeCustomer


# class ShipmentColumn(tables.Column):
#     def render(self, value, record):
#         return format_html('<a href="{}"><p class="text-left">{}</p></a>',
#                            reverse('shipment:shipment_detail', kwargs={'pk': record.shipment_id}),
#                            value)


class DischargeEntityTable(tables.Table):
    class Meta:
        model = DischargeEntity


class DischargeProviderTable(tables.Table):
    provider = tables.Column(verbose_name='Поставщик')
    shipment_id = tables.Column(verbose_name='Отгрузка')

    # def render_provider(self, record, value):
    #     return format_html('<a href="{}"><p class="text-left">{}</p></a>',
    #                        reverse('provider:provider_detail', kwargs={'pk': record.provider_id}),
    #                        value)

    def render_shipment_id(self, record, value):
        return format_html('<a href="{}"><p class="text-left">{}</p></a>',
                           reverse('shipment:shipment_edit', kwargs={'pk': record.shipment_id.pk}),
                           value)

    class Meta:
        model = DischargeProvider


class DischargeCustomerTable(tables.Table):
    customer = tables.Column(verbose_name='Заказчик')
    shipment_id = tables.Column(verbose_name='Отгрузка')

    # def render_customer(self, record, value):
    #     return format_html('<a href="{}"><p class="text-left">{}</p></a>',
    #                        reverse('customer:customer_detail', kwargs={'pk': record.customer_id}),
    #                        value)

    def render_shipment_id(self, record, value):
        return format_html('<a href="{}"><p class="text-left">{}</p></a>',
                           reverse('shipment:shipment_edit', kwargs={'pk': record.shipment_id.pk}),
                           value)

    class Meta:
        model = DischargeCustomer
