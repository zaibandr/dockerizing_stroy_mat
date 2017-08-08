# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from django.contrib.auth.decorators import login_required

from django.utils import timezone

from django_tables2 import RequestConfig
from .tables import OrdersTable, AvailableProviderTable, ProviderTable

from django.contrib.auth.models import User
from .models import Order, Provider, Zone
from .forms import NewOrderForm, UpdateOrderForm, EditOrderForm

import datetime

from geopy.geocoders import Yandex
from geopy.distance import vincenty
from shapely.geometry import Polygon, Point
import json

import requests


def home_page(request):
    redirect('/orders/')


def provider_notify(request):
    if request.method == 'POST':
        pks = request.POST.getlist('phone_number_checkbox')

        params = {
            'user': 'zaibandr@yandex.ru',
            'password': 'UHwOb0Bpd8hr3TE0ZauTBWneG59c',
            'to': '79057508337',
            'text': 'qwerty',
            'from': 'biznes',
            'answer': 'json'
        }

        url = 'https://gate.smsaero.ru/testsend/'

        order_id = request.POST.get('order_id')
        context = {
            'providers': ProviderTable(Provider.objects.filter(pk__in=pks)),
            'order_id': order_id
        }

        order = Order.objects.get(pk=order_id)
        if order.status == 'CRTD':
            order.status = 'PRCSG'
            order.save()
            resp = requests.get(url, params)
            context['resp'] = resp.json()
        else:
            context['prev_sent'] = True

        return render(request, 'has_app/providers.html', context)
    else:
        return HttpResponseForbidden


def new_order_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewOrderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            ###########################
            # set author field in form current user
            # https://stackoverflow.com/questions/18246326/in-django-how-do-i-set-user-field-in-form-to-the-currently-logged-in-user
            ###########################
            new_order = form.save(commit=False)

            new_order.manager = User.objects.get(username=request.user)

            geo_locator = Yandex()
            location = geo_locator.geocode(new_order.address, timeout=10)
            new_order.longitude = location.longitude
            new_order.latitude = location.latitude
            new_order.coordinate = location.point

            new_order.save()

            last_order_url = Order.objects.last().get_absolute_url()
            return HttpResponseRedirect(last_order_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewOrderForm()

    return render(request, "has_app/new_order.html", {'form': form})


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
        for provider in Provider.objects.all():
            polygon = Polygon(json.loads(provider.geo_json))
            if polygon.contains(point):
                point_within_provider.append(provider.pk)

        context['providers'] = AvailableProviderTable(Provider.objects.filter(pk__in=point_within_provider))


        # print(point_in_zone)

        # features = []
        # for zone in point_in_zone:
        #     feature = {
        #         'properties': {
        #             'fill': '#00FF00',
        #             'stroke-opacity': 0.9,
        #             'stroke-width': '5',
        #             'fill-opacity': 0.6,
        #             'stroke': '#ed4543',
        #             'description': zone.name
        #         },
        #         'id': len(features),
        #         'geometry': {
        #             'coordinates': [
        #                 zone.polygon
        #             ],
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
        #
        # context['geo_json'] = json.dumps(geo_json)

        return context


class OrderUpdate(UpdateView):
    model = Order
    form_class = UpdateOrderForm

    template_name_suffix = '_update_form'

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        print(request.POST)
        print(request.POST['time_completed'])
        if request.POST['status'] == 'CMPLTD' and request.POST['time_completed'] == '':
            request.POST['time_completed'] = datetime.datetime.now()
        return super(OrderUpdate, self).post(request, **kwargs)


class EditOrder(UpdateView):
    model = Order
    form_class = EditOrderForm
    template_name_suffix = '_edit_form'


class OrderCreate(CreateView):
    model = Order
    form_class = NewOrderForm

    template_name_suffix = '_create_form'
