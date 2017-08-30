from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden


from django.views.generic.edit import UpdateView

from django.contrib.auth.models import User, Group
from has_app.tables import ProviderTable
from has_app.models import Order, Provider, SmsNotify
from has_app.forms import UpdateOrderForm

import datetime

import requests

from notifications.signals import notify


def provider_notify(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)

        pks_checkbox = request.POST.getlist('phone_number_checkbox')
        provider_notified_pks = SmsNotify.objects.filter(order=order).values_list('provider', flat=True)
        pks = list(set(pks_checkbox).difference(set(provider_notified_pks)))

        url = 'https://gate.smsaero.ru/testsend/'
        for provider in Provider.objects.filter(pk__in=pks):
            params = {
                'user': 'zaibandr@yandex.ru',
                'password': 'UHwOb0Bpd8hr3TE0ZauTBWneG59c',
                'to': '79057508337',
                'text': 'qwerty',
                'from': 'biznes',
                'answer': 'json'
            }
            # sms_notify = SmsNotify.objects.get(order=order, provider=provider)
            # if sms_notify:
            #     continue
            # resp = requests.get(url, params)
            #
            # sms_notify = SmsNotify.objects.create(order=order, provider=provider, sms_id=resp.json()['id'])
            sms_notify = SmsNotify.objects.create(order=order, provider=provider, sms_id=100)
            sms_notify.save()

        # order_id = request.POST.get('order_id')
        context = {
            'providers': ProviderTable(Provider.objects.filter(pk__in=pks)),
            'order_id': pk
        }

        return redirect('order-detail', pk=order.pk)
    else:
        return HttpResponseForbidden


class OrderUpdate(UpdateView):
    model = Order
    form_class = UpdateOrderForm

    # template_name_suffix = '_update_form'
    template_name = 'has_app/supplier/order_update_form.html'

    def form_valid(self, form):
        # send notify
        notify.send(sender=User.objects.get(username=self.request.user),
                    recipient=User.objects.filter(groups=1),
                    verb='''Обновил(а) заказ 
                            <a href="{}">№{}</a>'''.format(
                            self.object.get_absolute_url(),
                            self.object.pk
                        )
                    )

        return super(OrderUpdate, self).form_valid(form)

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        print(request.POST)
        print(request.POST['time_completed'])
        if request.POST['provider'] == '0' or request.POST['cost'] == '0':
            request.POST['status'] = 'CRTD'
            request.POST['time_completed'] = None
        else:
            request.POST['time_completed'] = datetime.datetime.now()
        return super(OrderUpdate, self).post(request, **kwargs)
