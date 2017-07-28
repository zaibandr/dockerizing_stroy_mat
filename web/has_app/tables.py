import django_tables2 as tables
from django.utils.html import format_html
from .models import Order


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