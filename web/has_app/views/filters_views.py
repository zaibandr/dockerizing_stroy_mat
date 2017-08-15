from django.shortcuts import render

from django_filters.views import FilterView
from django_tables2 import SingleTableView
from has_app.tables import OrdersTable
from has_app.models import Order
from has_app.filters import OrderFilter


def order_filter_list(request):
    f = OrderFilter(request.GET, queryset=Order.objects.all())
    return render(request, 'has_app/order_filter.html', {'filter': f})


class FilteredOrderListView(FilterView, SingleTableView):
    table_class = OrdersTable
    model = Order
    template_name = 'has_app/filter_view.html'

    filterset_class = OrderFilter
