import django_tables2 as tables
from django.utils.html import format_html
from django.urls import reverse

from core.tables import PhoneNumberColumn
from .models import Customer


class CustomerNameColumn(tables.Column):
    def render(self, value, record):
        return format_html('<a href="{}"><p class="text-left">{}</p></a>',
                           reverse('customer:customer_detail', kwargs={'pk': record.pk}),
                           value)


class CustomerTable(tables.Table):
    name = CustomerNameColumn(verbose_name='Заказчик')
    phone_number = PhoneNumberColumn()

    class Meta:
        model = Customer
        fields = ('name', 'phone_number', 'contact_name',)