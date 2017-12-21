from django.contrib import admin
from haystack.admin import SearchModelAdmin
from .models import Customer, CreditPayment


def refresh_balance(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    for p in Customer.objects.filter(pk__in=selected):
        p.update_balance()

refresh_balance.short_description = "Обновить баланс"


class CustomerAdmin(SearchModelAdmin):
    fields = (
        'name', 'inn', 'contact_name',
        'phone_number', 'sms_phone_number', 'description',
        'saldo_debet', 'saldo_credit', 'saldo_date',
    )

    list_display = ('name', 'pk', 'balance', 'individual_person')
    list_filter = ('individual_person',)
    search_fields = ('pk', 'name')
    actions = [refresh_balance]


class CreditPaymentAdmin(SearchModelAdmin):
    list_display = ('customer', 'pk', 'amount', 'date', 'paid_date', 'paid', 'balance_add', 'balance_take_down')
    list_filter = ('date', 'paid_date', 'paid')

    def customer_name(self, obj):
        return obj.customer.name

    customer_name.short_description = 'Customer'
    customer_name.admin_order_field = 'customer__name'


admin.site.register(Customer, CustomerAdmin)
admin.site.register(CreditPayment, CreditPaymentAdmin)
