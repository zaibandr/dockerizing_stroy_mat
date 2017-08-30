from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView

from django_tables2 import RequestConfig
from django.utils import timezone

from django.contrib.auth.models import User
from has_app.tables import AvailableProviderTable, SimilarOrderTable, ProviderTable
from has_app.models import Order, Provider, Zone, Shipment, Comment, SmsNotify
from has_app.tables import OrdersTable, ShipmentTable, NotifiedProviders
from has_app.forms import CommentForm

from shapely.geometry import Polygon, Point
from geopy.distance import vincenty

import json

import random

from notifications.signals import notify


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
                name = 'provider_{}'.format(str(provider.pk))

                geo_data.append([polygon, name, popup, poly_coords, color])

        context['providers_table'] = AvailableProviderTable(Provider.objects.filter(pk__in=point_within_provider))

        similar_order = Order.objects.filter(
            provider_id__in=point_within_provider,
            status='CMPLTD',
            product_id=self.object.product.id
        )

        similar_order_pk = []
        d = {self.object.pk: True}
        this_order_coord = (self.object.longitude, self.object.latitude)
        dist = 2
        while len(similar_order_pk) < 5 and dist <= 10:
            for o in similar_order:
                if vincenty(this_order_coord, (o.longitude, o.latitude)).km < dist and o.pk not in d:
                    similar_order_pk.append(o.pk)
                    d[o.pk] = True
                if len(similar_order_pk) >= 5:
                    break
            dist += 2

        context['similar_order'] = SimilarOrderTable(Order.objects.filter(pk__in=similar_order_pk))

        sorted_geo_data = sorted(geo_data, key=lambda a: a[0].area, reverse=True)

        geo_data = [[name, popup, poly_coords, color]for _, name, popup, poly_coords, color in sorted_geo_data]
        context['geo_data'] = geo_data
        context['comments'] = Comment.objects.filter(order=self.object.pk)

        # notified_provider_pks = SmsNotify.objects.filter(order=self.object.pk).values('provider')
        # context['notified_providers'] = ProviderTable(Provider.objects.filter(pk__in=notified_provider_pks))
        context['notified_providers'] = NotifiedProviders(SmsNotify.objects.filter(order=self.object.pk))

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
    author = User.objects.get(username=request.user)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = author
            comment.order = order
            comment.save()

            if 'manager' in author.groups.values_list('name', flat=True):
                recipient_group = 'supplier'
            else:
                recipient_group = 'manager'

            notify.send(sender=author,
                        recipient=User.objects.filter(groups__name=recipient_group),
                        verb='''Добавил(а) коментарий к заказу 
                                <a href="{}">№{}</a>'''.format(
                                    order.get_absolute_url(),
                                    order.pk
                                )
                        )

            return redirect('order-detail', pk=order.pk)
    else:
        form = CommentForm()
    return render(request, 'has_app/add_comment_to_order.html', {'form': form})
