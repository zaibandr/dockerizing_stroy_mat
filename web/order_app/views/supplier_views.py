from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden


from django.views.generic.edit import UpdateView

from django.contrib.auth.models import User, Group
from order_app.models import Order, SmsNotify
from provider_app.models import Provider
from order_app.forms import UpdateOrderForm

import datetime

import requests

from notifications.signals import notify
from notifications.models import Notification


def provider_notify(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)

        pks_checkbox = request.POST.getlist('phone_number_checkbox')
        provider_notified_pks = SmsNotify.objects.filter(order=order).values_list('provider', flat=True)
        pks = list(set(pks_checkbox).difference(set(provider_notified_pks)))

        text = """Наименование: {}\nОбъем: {}\nАдрес: {}\nТонары: {}\nПрием: {}\nОплата: {}""".format(
            order.product.name,
            order.volume,
            order.address,
            order.get_tonar_display(),
            order.get_time_of_receipt_display(),
            order.get_payment_display()
        )
        url = 'https://gate.smsaero.ru/send/'
        for provider in Provider.objects.filter(pk__in=pks):
            params = {
                'user': 'direktor@domantis.ru',
                'password': 'tPajBaaiZL05iZBsmh0n2EObzrWL',
                'to': provider.phone_number,
                'text': text,
                'from': 'DOMANTIS',
                'answer': 'json'
            }
            resp = requests.get(url, params)
            try:
                sms_id = resp.json()['id']
            except KeyError:
                sms_id = 0

            sms_notify = SmsNotify.objects.create(order=order, provider=provider, sms_id=sms_id)
            # sms_notify = SmsNotify.objects.create(order=order, provider=provider, sms_id=100)
            sms_notify.save()

        return redirect('order:order_detail', pk=order.pk)
    else:
        return HttpResponseForbidden


def notify_cost(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)

        d = {k: v for k, v in request.POST.items() if k.startswith('cost_') and v != ''}
        pks = [int(i.replace('cost_', '')) for i in d.keys()]

        for sms_notify in SmsNotify.objects.filter(pk__in=pks):
            try:
                sms_notify.cost = int(d['cost_{}'.format(sms_notify.pk)])
            except ValueError as e:
                pass
            else:
                sms_notify.save()

        context = {
            'values': d
        }

        # return render(request, 'asda', context=context)
        return redirect('order:order_detail', pk=order.pk)
    else:
        return HttpResponseForbidden


class OrderUpdate(UpdateView):
    model = Order
    form_class = UpdateOrderForm

    # template_name_suffix = '_update_form'
    template_name = 'order_app/supplier/order_update_form.html'

    def form_valid(self, form):
        # send notify
        notify.send(sender=User.objects.get(username=self.request.user),
                    recipient=User.objects.get(pk=self.object.manager_id),
                    action_object=self.object,
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
            # Заказ обработан
            # Пометить прочитанными уведомления данного заказа для всех снабженцов
            group_name = User.objects.get(username=request.user).groups.values_list('name', flat=True)
            user_pks = User.objects.filter(groups__name=group_name).values_list('pk', flat=True)
            for n in Notification.objects.filter(
                                    recipient_id__in=user_pks,
                                    action_object_object_id=self.get_object().pk):
                n.mark_as_read()

            request.POST['time_completed'] = datetime.datetime.now()

        return super(OrderUpdate, self).post(request, **kwargs)
