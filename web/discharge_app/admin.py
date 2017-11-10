from django.contrib import admin
from .models import DischargeInput, DischargeCustomer, DischargeProvider


class DischargeInputAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'file_path')
    list_filter = ('date_time', )

    def file_path(self, obj):
        return obj.file.path

    file_path.short_description = 'file_path'


class DischargeCustomerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'pk', 'action', 'value', 'document_id', 'action_date', 'date')
    list_filter = ('date', 'action', )

    def customer_name(self, obj):
        return obj.customer.name

    customer_name.short_description = 'Customer'
    customer_name.admin_order_field = 'customer__name'


class DischargeProviderAdmin(admin.ModelAdmin):
    list_display = ('provider', 'pk', 'action', 'value', 'document_id', 'action_date', 'date')
    list_filter = ('date', 'action',)

    def provider_name(self, obj):
        return obj.provider.name

    provider_name.short_description = 'Provider'
    provider_name.admin_order_field = 'provider__name'


admin.site.register(DischargeInput, DischargeInputAdmin)
admin.site.register(DischargeCustomer, DischargeCustomerAdmin)
admin.site.register(DischargeProvider, DischargeProviderAdmin)
