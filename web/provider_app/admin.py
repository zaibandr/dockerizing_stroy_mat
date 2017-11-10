from django.contrib import admin
from haystack.admin import SearchModelAdmin

from .models import Provider


# Register your models here.


def make_hidden(modeladmin, request, queryset):
    queryset.update(hidden=True)

make_hidden.short_description = "Не показывать отмеченных поставщиков"


def make_unhidden(modeladmin, request, queryset):
    queryset.update(hidden=False)

make_unhidden.short_description = "Показывать отмеченных поставщиков"


class ProviderAdmin(SearchModelAdmin):
    fields = (
        'name', 'description', 'contact_name',
        'phone_number', 'sms_phone_number', 'mail_1', 'mail_2',
        'saldo_debet', 'saldo_credit', 'saldo_date',
        'regions', 'pick_points', 'hidden',
    )
    list_display = ('name', 'pk', 'contact_name', 'balance', 'orders_count', 'hidden')
    list_filter = ('hidden',)
    search_fields = ('pk', 'name', 'contact_name')
    actions = [make_hidden, make_unhidden]

admin.site.register(Provider, ProviderAdmin)
