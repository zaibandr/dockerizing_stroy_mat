from django.contrib import admin
from haystack.admin import SearchModelAdmin
from .models import Customer, CreditPayment


class CustomerAdmin(SearchModelAdmin):
    list_display = ('name', 'pk', 'balance', 'individual_person')
    list_filter = ('individual_person',)
    search_fields = ('pk', 'name')


class CreditPaymentAdmin(SearchModelAdmin):
    fields = (
        'name', 'contact_name',
        'phone_number', 'sms_phone_number', 'mail_1', 'mail_2', 'description',
        'saldo_debet', 'saldo_credit', 'saldo_date',
    )

    list_display = ('customer', 'pk', 'amount', 'date', 'paid_date', 'paid', 'balance_add', 'balance_take_down')
    list_filter = ('date', 'paid_date', 'paid')

    def customer_name(self, obj):
        return obj.customer.name

    customer_name.short_description = 'Customer'
    customer_name.admin_order_field = 'customer__name'


admin.site.register(Customer, CustomerAdmin)
admin.site.register(CreditPayment, CreditPaymentAdmin)
