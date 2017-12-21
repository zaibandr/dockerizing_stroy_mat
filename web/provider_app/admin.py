from django.contrib import admin
from haystack.admin import SearchModelAdmin

from .models import Provider
from provider_app.models import Region, PickPoint

# Register your models here.


def make_hidden(modeladmin, request, queryset):
    queryset.update(hidden=True)

make_hidden.short_description = "Не показывать отмеченных поставщиков"


def make_unhidden(modeladmin, request, queryset):
    queryset.update(hidden=False)

make_unhidden.short_description = "Показывать отмеченных поставщиков"


def refresh_balance(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    for p in Provider.objects.filter(pk__in=selected):
        p.update_balance()

refresh_balance.short_description = "Обновить баланс"


class RegionsInline(admin.TabularInline):
    model = Provider.regions.through
    verbose_name = "Связь: Регион доставки"
    verbose_name_plural = "Связи: Регионы доставок"


class PickPointsInline(admin.TabularInline):
    model = Provider.pick_points.through
    verbose_name = "Связь: Точка самовывоза"
    verbose_name_plural = "Связи: Точки самовывоза"


class ProviderAdmin(SearchModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'name', 'inn', 'contact_name', 'description',
                'phone_number', 'sms_phone_number', 'mail_1', 'mail_2',
                'saldo_debet', 'saldo_credit', 'saldo_date', 'hidden',
            )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('regions', 'pick_points'),
        }),
    )
    list_display = ('name', 'pk', 'contact_name', 'balance', 'orders_count', 'hidden')
    list_filter = ('hidden',)
    filter_horizontal = ('regions', 'pick_points', )
    search_fields = ('pk', 'name', 'contact_name', )
    inlines = [
        RegionsInline,
        PickPointsInline
    ]
    #exclude = ('regions', 'pick_points')
    view_on_site = True
    actions = [make_hidden, make_unhidden, refresh_balance]

admin.site.register(Provider, ProviderAdmin)
