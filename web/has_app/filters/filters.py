import django_filters
from django_filters import widgets
from has_app.models import Order
from django.contrib.auth.models import User


class OrderFilter(django_filters.FilterSet):
    date_from_to_range = django_filters.DateFromToRangeFilter(
        name='time_created',
        label='Дата создания',
        widget=widgets.RangeWidget(attrs={'placeholder': 'dd.mm.yyyy'}))

    date_range = django_filters.DateRangeFilter(name='time_created')
    address = django_filters.CharFilter(name='address', label='Адрес', lookup_expr='icontains')

    name = django_filters.CharFilter(name='name', label='Имя заказчика', lookup_expr='icontains')
    phone_number = django_filters.CharFilter(name='phone_number', label='Телефон', lookup_expr='icontains')

    volume = django_filters.RangeFilter(name='volume', widget=widgets.RangeWidget())

    manager = django_filters.ChoiceFilter(choices=User.objects.all().values_list('pk', 'username'))
    status = django_filters.ChoiceFilter(choices=Order.status_choice)
    tonar = django_filters.ChoiceFilter(choices=Order.tonar_choice)
    time_of_receipt = django_filters.ChoiceFilter(choices=Order.receipt_choice)

    class Meta:
        model = Order
        fields = []
