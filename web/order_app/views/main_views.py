from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.views.generic.detail import DetailView
from django_tables2 import RequestConfig

from order_app.viewmixins import CommentMixin, NotificationMixin, NearSimilarMixin
from order_app.models import Order
from order_app.tables import OrdersTable
from order_app.viewmixins import ProviderTableMixin, NotifiedProviderTableMixin, GeoJsonMixin


@login_required()
def orders(request, status='all'):
    if request.user.is_staff:
        all_orders_sqs = Order.objects.all().select_related('product')
    else:
        all_orders_sqs = Order.objects.filter(author=request.user).select_related('product')

    all_orders = OrdersTable(all_orders_sqs)

    RequestConfig(request).configure(all_orders)

    all_orders.paginate(page=request.GET.get('page', 1), per_page=10)

    # export_format = request.GET.get('_export', None)
    # if TableExport.is_valid_format(export_format):
    #     exporter = TableExport(export_format, all_orders)
    #     return exporter.response('table.{}'.format(export_format))

    context = {
        'orders': all_orders,
    }

    return render(request, 'order_app/order_list.html', context)


class OrderDetailView(NearSimilarMixin, CommentMixin, NotificationMixin, ProviderTableMixin,
                      GeoJsonMixin,
                      NotifiedProviderTableMixin, DetailView):

    model = Order

    # @cached_as(Provider, timeout=60*10)
    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        return context
