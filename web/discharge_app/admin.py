from django.contrib import admin
from .models import DischargeInput, DischargeCustomer, DischargeProvider, DischargeEntity, Entity


class DischargeInputAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'file_path')
    list_filter = ('date_time', )

    def file_path(self, obj):
        return obj.file.path

    file_path.short_description = 'file_path'


class DischargeCustomerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'pk', 'action', 'value', 'shipment_id', 'action_date', 'date')
    list_filter = ('date', 'action', 'customer__name')
    date_hierarchy = 'date'

    def customer_name(self, obj):
        return obj.customer.name

    customer_name.short_description = 'Customer'
    customer_name.admin_order_field = 'customer__name'


class DischargeProviderAdmin(admin.ModelAdmin):
    list_display = ('provider', 'pk', 'action', 'value', 'shipment_id', 'action_date', 'date')
    list_filter = ('date', 'action', 'provider__name')
    date_hierarchy = 'date'

    def provider_name(self, obj):
        return obj.provider.name

    provider_name.short_description = 'Provider'
    provider_name.admin_order_field = 'provider__name'


class DischargeEntityAdmin(admin.ModelAdmin):
    list_display = ('entity', 'pk', 'debet', 'credit', 'document_id', 'action_date', 'date')
    list_filter = ('date', 'entity__name')

    def entity_name(self, obj):
        return obj.entity.name

    entity_name.short_description = 'Entity'
    entity_name.admin_order_field = 'entity__name'


def add_as_customer(modeladmin, request, queryset):
    from customer_app.models import Customer
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    for e in Entity.objects.filter(pk__in=selected):
        c, created = Customer.objects.get_or_create(inn=e.inn, defaults={'name': e.name})


def add_as_provider(modeladmin, request, queryset):
    from provider_app.models import Provider
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    for e in Entity.objects.filter(pk__in=selected):
        p, created = Provider.objects.get_or_create(inn=e.inn, defaults={'name': e.name})


add_as_customer.short_description = "Дабавить отмеченные как Заказчики"
add_as_provider.short_description = "Дабавить отмеченные как Поставщики"


class EntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'inn')
    actions = [add_as_customer, add_as_provider]

admin.site.register(DischargeInput, DischargeInputAdmin)
admin.site.register(DischargeCustomer, DischargeCustomerAdmin)
admin.site.register(DischargeProvider, DischargeProviderAdmin)
admin.site.register(DischargeEntity, DischargeEntityAdmin)
admin.site.register(Entity, EntityAdmin)
