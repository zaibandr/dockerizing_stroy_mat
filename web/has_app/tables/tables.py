import django_tables2 as tables
from django.utils.html import format_html
from has_app.models import Order, Provider, Shipment, SmsNotify


class ProductColumn(tables.Column):
    def render(self, value, record):
        return format_html('<a href="/orders/{}/"><p class="text-left">{}</p></a>', record.pk, value)


class OrdersTable(tables.Table):
    product = ProductColumn(verbose_name='Product')

    class Meta:
        model = Order
        order_by = '-time_updated'

        # add class="paleblue" to <table> tag
        fields = ('id', 'product', 'volume', 'status', 'phone_number',
                  'address', 'manager', 'time_created', 'time_updated')

        row_attrs = {
            'class': lambda record: 'success' if record.status == 'CMPLTD' else 'warning' if record.status == 'PRCSG' else 'danger'
        }


class ProviderNameColumn(tables.Column):
    def render(self, value, record):
        return format_html('<a href="/providers/{}/"><p class="text-left">{}</p></a>', record.pk, value)


class ProviderTable(tables.Table):
    name = ProviderNameColumn(verbose_name='Поставщик')

    class Meta:
        model = Provider
        fields = ('phone_number', 'contact_name', 'name')


class AvailableProviderTable(tables.Table):
    phone_number_checkbox = tables.CheckBoxColumn(accessor='pk')
    name = ProviderNameColumn(verbose_name='Поставщик')

    class Meta:
        model = Provider
        fields = ('phone_number_checkbox', 'phone_number', 'contact_name', 'name')


class NotifiedProviders(tables.Table):
    provider_phone_number = tables.Column(accessor='provider.phone_number')
    provider_name = ProviderNameColumn(accessor='provider.name')
    provider_contact_name = tables.Column(accessor='provider.contact_name')
    # cost_input = tables.TemplateColumn(template)

    class Meta:
        model = SmsNotify
        fields = ('time_created', 'sms_id', 'cost')
        sequence = ('provider_phone_number', 'provider_contact_name',
                    'provider_name', 'time_created', 'sms_id')


class SimilarProviderNameColumn(tables.Column):
    def render(self, value, record):
        return format_html('<a href="/providers/{}/"><p class="text-left">{}</p></a>', record.provider_id, value)


class SimilarOrderTable(tables.Table):
    product = ProductColumn(verbose_name='Product')
    provider = SimilarProviderNameColumn(verbose_name='Поставщик')

    class Meta:
        model = Order
        fields = ('pk', 'product', 'cost', 'volume', 'address', 'provider_id', 'provider')


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
