import datetime
import json

import django.core.exceptions as dj_exceptions
from django.shortcuts import render
from django.urls import reverse

from customer_app.models import Customer
from provider_app.models import Provider
from .excel.excel_import import discharge_excel_to_json
from .forms import UploadFileForm
from .models import DischargeInput, DischargeCustomer, DischargeProvider, DischargeModel
from .models import DischargeEntity
from discharge_app.models import Entity


def upload_file(request):
    from collections import OrderedDict
    from core.utils import url_params_create

    def is_provider(name):
        try:
            Provider.objects.get(name=name)
            return True
        except dj_exceptions.ObjectDoesNotExist:
            return False

    def is_customer(name):
        try:
            Customer.objects.get(name=name)
            return True
        except dj_exceptions.ObjectDoesNotExist:
            return False

    # def discharge_create(**kwargs):
    #     from collections import OrderedDict
    #
    #     def is_provider(name):
    #         try:
    #             Provider.objects.get(name=name)
    #             return True
    #         except dj_exceptions.ObjectDoesNotExist:
    #             return False
    #
    #     def is_customer(name):
    #         try:
    #             Customer.objects.get(name=name)
    #             return True
    #         except dj_exceptions.ObjectDoesNotExist:
    #             return False
    #
    #     def is_credit(credit):
    #         return credit != ''
    #
    #     def is_debet(debet):
    #         return debet != ''
    #
    #     data = kwargs.copy()
    #
    #     if is_provider(data.get('name', '')):
    #         _object = Provider
    #         _discharge_object = DischargeProvider
    #         if is_credit(data.get('credit')):
    #             action = DischargeModel.ACTION_BALANCE_DOWN
    #         else:
    #             action = DischargeModel.ACTION_BALANCE_UP
    #     elif is_customer(data.get('name', '')):
    #         _object = Customer
    #         _discharge_object = DischargeCustomer
    #
    #         if is_credit(data.get('credit')):
    #             action = DischargeModel.ACTION_BALANCE_UP
    #         else:
    #             action = DischargeModel.ACTION_BALANCE_DOWN
    #     else:
    #         return 'unknown', OrderedDict(kwargs)
    #
    #     if is_credit(data.get('credit', '')):
    #         value = data.pop('credit')
    #         data.pop('debet')
    #     else:
    #         value = data.pop('debet')
    #         data.pop('credit')
    #
    #     dc_data = {
    #         _object.__name__.lower(): _object.objects.get(name=data.pop('name')),
    #         'action': action,
    #         'value': value
    #     }
    #     data.update(dc_data)
    #
    #     try:
    #         _discharge_object.objects.get(document_id=kwargs['document_id'])
    #     except dj_exceptions.ObjectDoesNotExist:
    #         _discharge_object.objects.create(**data)
    #     finally:
    #         return _object.__name__.lower(), OrderedDict(data)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = DischargeInput(file=request.FILES['file'])
            instance.date = datetime.datetime.now().date()
            instance.save()

            latest_upload = DischargeInput.objects.last()

            transaction_dicts = json.loads(discharge_excel_to_json(latest_upload.file.path))

            unknowns = []
            customers = []
            providers = []

            for d in transaction_dicts:

                #############################################################
                # Загрузка всех транзакций
                #############################################################
                E, created = Entity.objects.get_or_create(inn=d['inn'], defaults={'name': d['name']})
                if len(E.name) >= len(d['name']):
                    E.name = d['name']
                    E.save()
                try:
                    DischargeEntity.objects.get(document_id=d['document_id'])
                except dj_exceptions.ObjectDoesNotExist:
                    discharge_entity_data = d.copy()
                    discharge_entity_data.pop('name')
                    discharge_entity_data.pop('inn')

                    DischargeEntity.objects.create(entity=E, **discharge_entity_data)
                #############################################################

                data = OrderedDict(d)
                if is_customer(d['name']):
                    customers.append(data.items())
                elif is_provider(d['name']):
                    providers.append(data.items())
                else:
                    # '?{}'.format('&'.join(['{}={}'.format(k, v) for k, v in d.items()]))

                    provider_add_url = reverse('admin:provider_app_provider_add') + url_params_create(**data)
                    customer_add_url = reverse('admin:customer_app_customer_add') + url_params_create(**data)
                    unknowns.append(
                        sorted(data.items()) + [
                            ('provider_add', provider_add_url),
                            ('customer_add', customer_add_url)
                        ]
                    )

            context = {
                'unknowns': unknowns,
                'customers': customers,
                'providers': providers
            }
            return render(request, 'discharge_app/uploaded.html', context=context)
    else:
        form = UploadFileForm()
    return render(request, 'discharge_app/upload.html', {'form': form})