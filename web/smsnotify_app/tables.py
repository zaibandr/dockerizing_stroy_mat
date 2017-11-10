import django_tables2 as tables
import requests
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from core.tables import PhoneNumberColumn
from smsnotify_app.models import SmsNotify


class NotifiedProviders(tables.Table):
    provider_phone_number = PhoneNumberColumn(accessor='provider.phone_number')
    provider_name = tables.Column(accessor='provider.name')
    provider_contact_name = tables.Column(accessor='provider.contact_name')
    sms_id = tables.Column()
    cost = tables.Column(verbose_name='Стоймость')

    def render_provider_name(self, record, value):
        return format_html('<a href="{}"><p class="text-left">{}</p></a>',
                           reverse('provider:provider_detail', kwargs={'pk': record.provider.pk}),
                           value)

    def render_sms_id(self, record, value):
        status = {
            'delivery success': 'Сообщение доставлено',
            'delivery failure': 'Ошибка доставки SMS',
            'smsc submit': 'Сообщение передано оператору',
            'smsc reject': 'Сообщение отклонено',
            'queue': 'Ожидает отправки',
            'wait status': 'Ожидание статуса (запросите позднее)',
            'incorrect id. reject': 'Неверный идентификатор сообщения',
            'empty field. reject': 'Не все обязательные поля заполнены',
            'incorrect user or password. reject': 'Ошибка авторизации',
        }

        url = 'https://gate.smsaero.ru/status/'
        params = {
            'user': 'direktor@domantis.ru',
            'password': 'tPajBaaiZL05iZBsmh0n2EObzrWL',
            'id': int(value),
            'answer': 'json'
        }
        resp = requests.get(url, params)
        try:
            value = status[resp.json()['result']]
        except KeyError:
            value = resp.json()

        return value

    def render_cost(self, record, value):
        html = """<input type="text" placeholder="Цена" class="form-control col-md-4" name="cost_{}" value="{}">""".format(
            record.pk, value
        )

        return mark_safe(html)

    class Meta:
        model = SmsNotify
        fields = ('time_created', 'sms_id')
        sequence = ('provider_phone_number', 'provider_contact_name',
                    'provider_name', 'time_created', 'sms_id', 'cost')