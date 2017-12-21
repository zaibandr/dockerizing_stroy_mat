from django.shortcuts import render
from django.views.generic.detail import DetailView
from django_filters.views import FilterView
from django_tables2 import RequestConfig
from django_tables2 import SingleTableView

from order_app.models import Order
from order_app.tables import SimilarOrderTable as ProviderOrderTable

from discharge_app.viewmixins import TransactionsMixin

from shipment_app.models import Shipment
from shipment_app.tables import ShipmentTable

from .filters import ProviderFilter
from .models import Provider
from .tables import ProviderTable


class ProviderDetailView(TransactionsMixin, DetailView):
    model = Provider
    template_name = 'provider_app/provider_detail.html'

    def get_context_data(self, *args, **kwargs):
        import json
        self.object.update_balance()

        context = super(ProviderDetailView, self).get_context_data(*args, **kwargs)
        geo_json = {
            "type": "FeatureCollection",
            "features": []
        }

        for region in self.object.regions.all():
            feature = {
                "type": "Feature",
                "properties": {
                    "popup": '<a href="{}" >{}</a>'.format(self.object.get_absolute_url(), region.description),
                    "color": 'DarkRed',
                    "fillColor": 'DarkBlue',
                    "fillOpacity": 0.1
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": region.delivery_region['coordinates']
                }
            }

            geo_json['features'].append(feature)

        # d = {}
        # for o in Order.objects.filter(product_id=1, provider_id=self.object.pk):
        #     if o.cost not in d:
        #         d[o.cost] = [o]
        #     else:
        #         d[o.cost] += [o]
        #
        # cost_center = {}
        # for k, v in d.items():
        #     cost_center[k] = [sum([o.latitude for o in v])/len(v), sum([o.longitude for o in v])/len(v)]

        provider_orders = Order.objects.filter(provider_id=self.object.pk).order_by('cost', 'address') \
            .select_related('provider', 'product')

        context['geo_json'] = json.dumps(geo_json)
        context['provider_orders'] = provider_orders
        context['provider_orders_table'] = ProviderOrderTable(provider_orders)

        context['shipments_table'] = ShipmentTable(Shipment.objects.filter(provider=self.object.pk))

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