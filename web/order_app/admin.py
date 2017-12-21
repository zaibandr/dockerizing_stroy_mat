import datetime

from django.contrib import admin
from haystack.admin import SearchModelAdmin

from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget

from .models import Order


def order_refresh(modeladmin, request, queryset):
    queryset.update(time_updated=datetime.datetime.now())

order_refresh.short_description = "Обновить отмеченные заказы"


class OrderAdmin(SearchModelAdmin):
    list_display = ('pk', 'product', 'volume', 'status', 'address', 'phone_number', 'created')
    list_filter = ('status', 'created',)
    search_fields = ('address', 'provider__name', 'product__name', 'description')
    date_hierarchy = 'created'
    view_on_site = True
    actions = [order_refresh]

    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }

admin.site.register(Order, OrderAdmin)