from django.shortcuts import render
from django.views.generic.detail import DetailView
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required

from .models import Customer
from .tables import CustomerTable


@login_required()
#@cached_as(Order, timeout=60*5)
def customers(request, status='all'):
    all_customers = CustomerTable(Customer.objects.all())

    RequestConfig(request).configure(all_customers)

    all_customers.paginate(page=request.GET.get('page', 1), per_page=10)

    # export_format = request.GET.get('_export', None)
    # if TableExport.is_valid_format(export_format):
    #     exporter = TableExport(export_format, all_customers)
    #     return exporter.response('table.{}'.format(export_format))

    context = {
        'customers': all_customers,
    }

    return render(request, 'customer_app/customer_list.html', context)


class CustomerDetailView(DetailView):

    model = Customer

    # @cached_as(Provider, timeout=60*10)
    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)

        return context
