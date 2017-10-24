from django_filters.views import FilterView
from django_tables2 import SingleTableView
from order_app.tables import OrdersTable
from order_app.models import Order
from order_app.filters import OrderFilter
from cacheops import cached_as, cached_view_as


class FilteredOrderListView(FilterView, SingleTableView):
    table_class = OrdersTable
    model = Order
    template_name = 'order_app/filter_view.html'

    filterset_class = OrderFilter

    table_pagination = {
        'per_page': 50
    }

orders_filter = cached_view_as(Order)(FilteredOrderListView.as_view())
