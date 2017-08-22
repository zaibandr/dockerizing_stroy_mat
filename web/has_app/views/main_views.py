from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView

from django_tables2 import RequestConfig
from django.utils import timezone

from django.contrib.auth.models import User
from has_app.tables import AvailableProviderTable, SimilarOrderTable
from has_app.models import Order, Provider, Zone, Shipment, Comment
from has_app.tables import OrdersTable, ShipmentTable
from has_app.forms import CommentForm

from shapely.geometry import Polygon, Point
import json

import random


@login_required()
def orders(request, status='all'):
    if request.user.is_staff:
        all_orders_sqs = Order.objects.all()
    else:
        all_orders_sqs = Order.objects.filter(manager=request.user)

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
        for provider in Provider.objects.filter(products__id__exact=self.object.product.id):
            polygon = Polygon(provider.geom['coordinates'][0])
            if polygon.contains(point):
                point_within_provider.append(provider.pk)

                color = random.choice(
                    [
                        'Red', 'DarkRed', 'Yellow', 'OrangeRed',
                        'Blue', 'DarkBlue', 'DeepSkyBlue', 'DeepPink',
                        'Green', 'Lime', 'SpringGreen', 'Black'
                     ]
                )
                popup = '<a href="{}" >{}</a>'.format(provider.get_absolute_url(), provider.name)
                poly_coords = [[p[1], p[0]]for p in provider.geom['coordinates'][0]]

                geo_data.append([polygon, popup, poly_coords, color])

        context['providers_table'] = AvailableProviderTable(Provider.objects.filter(pk__in=point_within_provider))

        similar_order = Order.objects.filter(
            provider_id__in=point_within_provider,
            status='CMPLTD',
            product_id=self.object.product.id
        )

        context['similar_order'] = SimilarOrderTable(similar_order)

        sorted_geo_data = sorted(geo_data, key=lambda a: a[0].area, reverse=True)

        geo_data = [[pr, poly_coords, clr]for _, pr, poly_coords, clr in sorted_geo_data]
        context['geo_data'] = geo_data
        context['comments'] = Comment.objects.filter(order=self.object.pk)

        return context


class ProviderDetailView(DetailView):
    model = Provider
    template_name = 'has_app/provider_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProviderDetailView, self).get_context_data(**kwargs)
        context['poly_coord'] = [[p[1], p[0]]for p in self.object.geom['coordinates'][0]]

        context['provider_orders'] = SimilarOrderTable(Order.objects.filter(provider_id=self.object.pk))

        return context


@login_required()
def shipments(request, status='all'):
    if request.user.is_staff:
        all_shipment_sqs = Shipment.objects.all()
    else:
        all_shipment_sqs = Shipment.objects.filter(manager=request.user)

    all_shipment = ShipmentTable(all_shipment_sqs)

    RequestConfig(request).configure(all_shipment)
    all_shipment.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'shipments': all_shipment,
    }

    return render(request, 'has_app/shipments.html', context)


def add_comment_to_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = User.objects.get(username=request.user)
            comment.order = order
            comment.save()
            return redirect('order-detail', pk=order.pk)
    else:
        form = CommentForm()
    return render(request, 'has_app/add_comment_to_order.html', {'form': form})
