from django.shortcuts import render
from django.views.generic.detail import DetailView
from django_filters.views import FilterView
from django_tables2 import RequestConfig
from django_tables2 import SingleTableView

from order_app.models import Order
from order_app.tables import SimilarOrderTable as ProviderOrderTable
from .filters import ProviderFilter
from .models import Provider
from .tables import ProviderTable


class ProviderDetailView(DetailView):
    model = Provider
    template_name = 'provider_app/provider_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProviderDetailView, self).get_context_data(*args, **kwargs)
        context['poly_coord'] = [[p[1], p[0]]for p in self.object.geom['coordinates'][0]]

        d = {}
        for o in Order.objects.filter(product_id=1, provider_id=self.object.pk):
            if o.cost not in d:
                d[o.cost] = [o]
            else:
                d[o.cost] += [o]

        cost_center = {}
        for k, v in d.items():
            cost_center[k] = [sum([o.latitude for o in v])/len(v), sum([o.longitude for o in v])/len(v)]

        provider_orders = Order.objects.filter(provider_id=self.object.pk).order_by('cost', 'address')

        context['cost_center'] = cost_center
        context['provider_orders'] = provider_orders
        context['provider_orders_table'] = ProviderOrderTable(provider_orders)

        return context


def provider_list(request):

    providers_table = ProviderTable(Provider.objects.all().exclude(pk=0))

    RequestConfig(request).configure(providers_table)

    providers_table.paginate(page=request.GET.get('page', 1), per_page=25)

    context = {
        'providers_table': providers_table,
    }

    return render(request, 'provider_app/provider_list.html', context)


class FilteredProviderListView(FilterView, SingleTableView):
    table_class = ProviderTable
    model = Provider
    template_name = 'provider_app/provider_filter.html'

    filterset_class = ProviderFilter

    table_pagination = {
        'per_page': 50
    }