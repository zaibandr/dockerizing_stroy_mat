from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from django_tables2 import RequestConfig
from django.utils import timezone

from django.contrib.auth.models import User
from notifications.models import Notification

from order_app.models import Order, SmsNotify, Comment
from provider_app.models import Provider

from order_app.tables import SimilarOrderTable, OrdersTable
from provider_app.tables import AvailableProviderTable, NotifiedProviders
from order_app.forms import CommentForm

from shapely.geometry import Polygon, Point
from geopy.distance import vincenty


import random

from notifications.signals import notify

from cacheops import cached_as, cached_view_as


@login_required()
#@cached_as(Order, timeout=60*5)
def orders(request, status='all'):
    if request.user.is_staff:
        all_orders_sqs = Order.objects.all()
    else:
        all_orders_sqs = Order.objects.filter(manager=request.user)

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


class OrderDetailView(DetailView):

    model = Order

    # @cached_as(Provider, timeout=60*10)
    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['unread_notifications'] = Notification.objects.filter(
            recipient=self.request.user,
            action_object_object_id=self.object.pk,
            unread=True)

        # # distance context
        # geo_locator = Yandex()
        # center = geo_locator.geocode('Москва', timeout=10)
        #
        # loc_coord = (self.object.latitude, self.object.longitude)
        # center_coord = (center.latitude, center.longitude)
        #
        # context['distance'] = '{} km'.format(vincenty(loc_coord, center_coord).km)
        # #########################################################################

        # ##########################################################################
        # point_in_zone = []
        # point = Point((self.object.longitude, self.object.latitude))
        # for zone in Zone.objects.all():
        #     polygon = Polygon(json.loads(zone.polygon))
        #     if polygon.contains(point):
        #         point_in_zone.append(zone)
        #
        # context['point_in_zone'] = point_in_zone

        #@cached_as(Order, timeout=60*60)
        def build_geo_data(order):
            point_within_provider = []
            geo_data = []

            for provider in Provider.objects.filter(products__id__exact=order.product.id):
                polygon = Polygon(provider.geom['coordinates'][0])
                if polygon.contains(Point(order.longitude, order.latitude)):
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

            sorted_geo_data = sorted(geo_data, key=lambda a: a[0].area, reverse=True)

            geo_data = [[name, popup, poly_coords, color] for _, name, popup, poly_coords, color in sorted_geo_data]

            return point_within_provider, geo_data

        #@cached_as(Order, timeout=60*60)
        def get_near(order):
            near_valid_distance_10_km = []
            near_valid_distance_20_km = []
            near_valid_distance_30_km = []
            d = {order.pk: True}
            this_order_coord = (order.longitude, order.latitude)

            similar_order_all = Order.objects.filter(
                # provider_id__in=point_within_provider,
                status='CMPLTD',
                product_id=order.product.id
            )

            for o in similar_order_all:
                if o.pk in d:
                    continue
                # if len(near_valid_distance_10_km) + len(near_valid_distance_20_km) + len(near_valid_distance_30_km) >= 15:
                #     break
                distance = vincenty(this_order_coord, (o.longitude, o.latitude)).km
                if distance < 10:
                    near_valid_distance_10_km.append(o.pk)
                    d[o.pk] = True
                elif distance < 20:
                    near_valid_distance_20_km.append(o.pk)
                    d[o.pk] = True
                elif distance < 30:
                    near_valid_distance_30_km.append(o.pk)
                    d[o.pk] = True
            return near_valid_distance_10_km, near_valid_distance_20_km, near_valid_distance_30_km

        near_valid_distance_10_km, near_valid_distance_20_km, near_valid_distance_30_km = get_near(self.object)

        near_similar_order_10_km = Order.objects.filter(pk__in=near_valid_distance_10_km).order_by('address', 'cost')
        context['near_similar_order_10_km'] = near_similar_order_10_km
        context['near_similar_order_10_km_table'] = SimilarOrderTable(near_similar_order_10_km)

        near_similar_order_20_km = Order.objects.filter(pk__in=near_valid_distance_20_km).order_by('address', 'cost')
        context['near_similar_order_20_km'] = near_similar_order_20_km
        context['near_similar_order_20_km_table'] = SimilarOrderTable(near_similar_order_20_km)

        near_similar_order_30_km = Order.objects.filter(pk__in=near_valid_distance_30_km).order_by('address', 'cost')
        context['near_similar_order_30_km'] = near_similar_order_30_km
        context['near_similar_order_30_km_table'] = SimilarOrderTable(near_similar_order_30_km)

        point_within_provider, geo_data = build_geo_data(self.object)

        context['providers_table'] = AvailableProviderTable(
            Provider.objects.filter(pk__in=point_within_provider, hidden=False)
        )
        context['geo_data'] = geo_data
        context['comments'] = Comment.objects.filter(order=self.object.pk)

        context['notified_providers'] = NotifiedProviders(SmsNotify.objects.filter(order=self.object.pk))

        return context


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
                recipient = User.objects.filter(groups__name='supplier')
            else:
                recipient = User.objects.get(pk=order.manager_id)

            notify.send(sender=author,
                        recipient=recipient,
                        action_object=order,
                        verb='''Добавил(а) коментарий к заказу 
                                <a href="{}">№{}</a>'''.format(
                                    order.get_absolute_url(),
                                    order.pk
                                )
                        )

            # обновление заказа чтоб поднялся на самый верх
            order.save()

            return redirect('order:order_detail', pk=order.pk)
    else:
        form = CommentForm()
    return render(request, 'order_app/add_comment_to_order.html', {'form': form})


class EditComment(UpdateView):
    model = Comment
    form_class = CommentForm
    # template_name_suffix = '_edit_form'
    template_name = 'order_app/update_comment.html'
