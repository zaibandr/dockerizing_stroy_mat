import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html

from core.tables import PhoneNumberColumn
from .models import Provider


class ProviderNameColumn(tables.Column):
    def render(self, value, record):
        return format_html('<a href="{}"><p class="text-left">{}</p></a>',
                           reverse('provider:provider_detail', kwargs={'pk': record.pk}),
                           value)


class ProviderTable(tables.Table):
    name = ProviderNameColumn(verbose_name='Поставщик')
    phone_number = PhoneNumberColumn()

    class Meta:
        model = Provider
        fields = ('name', 'phone_number', 'contact_name',)


class AvailableProviderTable(tables.Table):
    phone_number_checkbox = tables.CheckBoxColumn(accessor='pk')
    phone_number = PhoneNumberColumn()
    name = ProviderNameColumn(verbose_name='Поставщик')

    class Meta:
        model = Provider
        fields = ('phone_number_checkbox', 'phone_number', 'contact_name', 'name')