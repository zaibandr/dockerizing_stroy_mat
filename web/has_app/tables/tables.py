import django_tables2 as tables
from django.utils.html import format_html
from has_app.models import Order, Provider


class ProductColumn(tables.Column):
    def render(self, value, record):
        return format_html('<a href="/orders/{}/"><p class="text-left">{}</p></a>', record.pk, value)


class OrdersTable(tables.Table):
    product = ProductColumn(verbose_name='Product')

    class Meta:
        model = Order
        order_by = '-time_created'

        # add class="paleblue" to <table> tag
        fields = ('id', 'product', 'volume', 'status', 'phone_number', 'address', 'time_created')


class ProviderTable(tables.Table):
    name = tables.Column(verbose_name='Поставщик')

    class Meta:
        model = Provider
        fields = ('phone_number', 'contact_name', 'name')


class AvailableProviderTable(tables.Table):
    phone_number_checkbox = tables.CheckBoxColumn(accessor='pk')
    name = tables.Column(verbose_name='Поставщик')

    class Meta:
        model = Provider
        fields = ('phone_number_checkbox', 'phone_number', 'contact_name', 'name')


class SimilarOrderTable(tables.Table):

    class Meta:
        model = Order
        fields = ('pk', 'product', 'cost', 'volume', 'address', 'provider_id', 'provider')