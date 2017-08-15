from django.shortcuts import render
from django.http import HttpResponseForbidden


from django.views.generic.edit import UpdateView

from has_app.tables import ProviderTable
from has_app.models import Order, Provider
from has_app.forms import UpdateOrderForm

import datetime

import requests


def provider_notify(request, pk):
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

        # order_id = request.POST.get('order_id')
        context = {
            'providers': ProviderTable(Provider.objects.filter(pk__in=pks)),
            'order_id': pk
        }

        order = Order.objects.get(pk=pk)
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