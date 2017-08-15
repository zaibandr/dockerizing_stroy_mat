from django_filters import FilterSet
from has_app.models import Order


class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = ['volume', 'status', 'address', 'name', 'tonar',
                  'time_of_receipt', 'phone_number', 'time_created']
