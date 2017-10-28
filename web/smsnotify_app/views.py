import requests
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect

from order_app.models import Order
from provider_app.models import Provider
from smsnotify_app.models import SmsNotify


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