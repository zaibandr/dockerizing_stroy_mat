from django_filters.views import FilterView
from django_tables2 import SingleTableView

from order_app.models import Order
from order_app.filters import OrderFilter
from order_app.tables import OrdersTable


class FilteredOrderListView(FilterView, SingleTableView):
    use_for_related_fields = True

    table_class = OrdersTable
    model = Order
    template_name = 'order_app/filter_view.html'

    filterset_class = OrderFilter

    def get_queryset(self):
        return self.model.objects.all().select_related('product', 'provider')

    table_pagination = {
        'per_page': 50
    }

    def get_context_data(self, **kwargs):
        context = super(FilteredOrderListView, self).get_context_data(**kwargs)

        return context
