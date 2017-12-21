from django.shortcuts import render
from django.views.generic.detail import DetailView
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required

from discharge_app.viewmixins import TransactionsMixin

from shipment_app.models import Shipment
from shipment_app.tables import ShipmentTable

from .models import Customer
from .tables import CustomerTable


@login_required()
#@cached_as(Order, timeout=60*5)
def customers(request, status='all'):
    all_customers = CustomerTable(Customer.objects.all())

    RequestConfig(request).configure(all_customers)

    all_customers.paginate(page=request.GET.get('page', 1), per_page=20)

    # export_format = request.GET.get('_export', None)
    # if TableExport.is_valid_format(export_format):
    #     exporter = TableExport(export_format, all_customers)
    #     return exporter.response('table.{}'.format(export_format))

    context = {
        'customers_table': all_customers,
    }

    return render(request, 'customer_app/customer_list.html', context)


class CustomerDetailView(TransactionsMixin, DetailView):

    model = Customer

    # @cached_as(Provider, timeout=60*10)
    def get_context_data(self, **kwargs):
        self.object.update_balance()

        context = super(CustomerDetailView, self).get_context_data(**kwargs)

        context['shipments_table'] = ShipmentTable(Shipment.objects.filter(customer=self.object.pk))
        return context
