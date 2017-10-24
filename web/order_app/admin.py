from django.contrib import admin
from haystack.admin import SearchModelAdmin
from .models import Order, Comment, SmsNotify
import datetime


def order_refresh(modeladmin, request, queryset):
    queryset.update(time_updated=datetime.datetime.now())

order_refresh.short_description = "Обновить отмеченные заказы"


class OrderAdmin(SearchModelAdmin):
    list_display = ('pk', 'product', 'volume', 'status', 'address', 'tonar', 'phone_number', 'time_created')
    list_filter = ('status', 'time_created',)
    search_fields = ('address', 'provider__name', 'product__name', 'description')
    actions = [order_refresh]

admin.site.register(Order, OrderAdmin)


class CommentAdmin(SearchModelAdmin):
    list_display = ('order_id', 'author', 'text', 'time_created')
    list_filter = ('author__username', 'time_created',)
    search_fields = ('text', )

admin.site.register(Comment, CommentAdmin)


class SmsNotifyAdmin(SearchModelAdmin):
    list_display = ('order_id', 'provider', 'sms_id', 'cost', 'time_created')
    list_filter = ('time_created',)

admin.site.register(SmsNotify, SmsNotifyAdmin)