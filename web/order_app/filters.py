import django_filters
from django.contrib.auth.models import User
from django.forms import Select
from django_filters import widgets

from product_app.models import Product
from provider_app.models import Provider
from .models import Order


class MySelect(Select):
    def render_option(self, selected_choices, option_value, option_label):
        # look at the original for something to start with
        return '<option value="{}" data-tokens="{}">{}</option>'.format(option_value, str(option_label).lower(), option_label)


class OrderFilter(django_filters.FilterSet):
    date_from_to_range = django_filters.DateFromToRangeFilter(
        name='created',
        label='Дата создания',
        widget=widgets.RangeWidget(attrs={'placeholder': 'dd.mm.yyyy'}))

    date_range = django_filters.DateRangeFilter(name='created')
    address = django_filters.CharFilter(name='address', label='Адрес', lookup_expr='icontains')

    name = django_filters.CharFilter(name='name', label='Имя заказчика', lookup_expr='icontains')
    phone_number = django_filters.CharFilter(name='phone_number', label='Телефон', lookup_expr='icontains')

    volume = django_filters.RangeFilter(name='volume')

    product = django_filters.ChoiceFilter(
        choices=Product.objects.all().values_list('pk', 'name'),
        widget=MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    provider = django_filters.ChoiceFilter(
        choices=Provider.objects.all().values_list('pk', 'name'),
        widget=MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    author = django_filters.ChoiceFilter(choices=User.objects.all().values_list('pk', 'username'))
    status = django_filters.ChoiceFilter(choices=Order.status_choice)
    tonar = django_filters.ChoiceFilter(choices=Order.tonar_choice)
    time_of_receipt = django_filters.ChoiceFilter(choices=Order.receipt_choice)

    class Meta:
        model = Order
        fields = []
