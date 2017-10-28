from django.contrib import admin
from haystack.admin import SearchModelAdmin

from .models import SmsNotify


class SmsNotifyAdmin(SearchModelAdmin):
    list_display = ('order_id', 'provider', 'sms_id', 'cost', 'time_created')
    list_filter = ('time_created',)

admin.site.register(SmsNotify, SmsNotifyAdmin)
