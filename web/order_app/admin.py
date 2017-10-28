import datetime

from django.contrib import admin
from haystack.admin import SearchModelAdmin

from .models import Order


def order_refresh(modeladmin, request, queryset):
    queryset.update(time_updated=datetime.datetime.now())

order_refresh.short_description = "Обновить отмеченные заказы"


class OrderAdmin(SearchModelAdmin):
    list_display = ('pk', 'product', 'volume', 'status', 'address', 'tonar', 'phone_number', 'created')
    list_filter = ('status', 'created',)
    search_fields = ('address', 'provider__name', 'product__name', 'description')
    actions = [order_refresh]

admin.site.register(Order, OrderAdmin)