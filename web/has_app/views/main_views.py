from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView

from django_tables2 import RequestConfig
from django.utils import timezone

from has_app.tables import AvailableProviderTable, SimilarOrderTable
from has_app.models import Order, Provider, Zone
from has_app.tables import OrdersTable

from shapely.geometry import Polygon, Point
import json

import random


@login_required()
def orders(request, status='all'):
    all_orders_sqs = Order.objects.all()

    all_orders = OrdersTable(all_orders_sqs)

    RequestConfig(request).configure(all_orders)
    all_orders.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'orders': all_orders,
    }

    return render(request, 'has_app/orders.html', context)


class OrderDetailView(DetailView):

    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        # # distance context
        # geo_locator = Yandex()
        # center = geo_locator.geocode('Москва', timeout=10)
        #
        # loc_coord = (self.object.latitude, self.object.longitude)
        # center_coord = (center.latitude, center.longitude)
        #
        # context['distance'] = '{} km'.format(vincenty(loc_coord, center_coord).km)
        # #########################################################################

        point_in_zone = []
        point = Point((self.object.longitude, self.object.latitude))
        for zone in Zone.objects.all():
            # print(zone, zone.polygon)

            polygon = Polygon(json.loads(zone.polygon))
            if polygon.contains(point):
                point_in_zone.append(zone)

        context['point_in_zone'] = point_in_zone

        point_within_provider = []
        geo_data = []
        for provider in Provider.objects.all():
            polygon = Polygon(provider.geom['coordinates'][0])
            if polygon.contains(point):
                point_within_provider.append(provider.pk)

                hex_color = [hex(random.randrange(0, 255))[2:] for _ in range(3)]
                color = '#{}'.format(''.join(hex_color))
                poly = [[p[1], p[0]]for p in provider.geom['coordinates'][0]]

                geo_data.append([provider.name, poly, color])

        context['providers_table'] = AvailableProviderTable(Provider.objects.filter(pk__in=point_within_provider))
        # context['polygon_coords'] = polygon_coords

        similar_order = Order.objects.filter(status='CMPLTD').filter(provider_id__in=point_within_provider)
        context['similar_order'] = SimilarOrderTable(similar_order)

        # features = []
        # for p in data:
        #     feature = {
        #         'properties': {
        #             'fill': '#00FF00',
        #             'stroke-opacity': 0.9,
        #             'stroke-width': '5',
        #             'fill-opacity': 0.6,
        #             'stroke': '#ed4543',
        #             'description': p.name
        #         },
        #         'id': len(features),
        #         'geometry': {
        #             'coordinates': p.geom,
        #             'type': 'Polygon'
        #         },
        #         'type': 'Feature'
        #     }
        #     features.append(feature)
        #
        # # print(features)
        #
        # geo_json = {
        #     'type': 'FeatureCollection',
        #     'features': features
        # }

        context['geo_data'] = geo_data

        return context
