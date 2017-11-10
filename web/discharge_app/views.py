import datetime
import json

import django.core.exceptions as dj_exceptions
from django.shortcuts import render

from customer_app.models import Customer
from provider_app.models import Provider
from .excel.excel_import import discharge_excel_to_json
from .forms import UploadFileForm
from .models import DischargeInput, DischargeCustomer, DischargeProvider


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # if len(DischargeInput.objects.filter(date=datetime.datetime.now().date())) != 0:
            #     context = {'json': {'error': 'Сегодня уже была загружена выписка'}}
            #
            #     return render(request, 'discharge_app/uploaded.html', context=context)

            instance = DischargeInput(file=request.FILES['file'])
            instance.date = datetime.datetime.now().date()
            instance.save()

            latest_upload = DischargeInput.objects.last()

            data = json.loads(discharge_excel_to_json(latest_upload.file.path))

            errors = []
            success = []

            for d in data:
                if d['credit'] != '':
                    try:
                        customer = Customer.objects.get(name=d['name'])
                    except dj_exceptions.ObjectDoesNotExist:
                        errors.append({d['name']: 'Не удалось найти объект с именем: {}'.format(d['name'])})
                    else:
                        try:
                            dc = DischargeCustomer.objects.get(document_id=d['document_id'])
                        except dj_exceptions.ObjectDoesNotExist:
                            success.append(d)
                            dc = DischargeCustomer.objects.create(
                                customer=customer,
                                action=DischargeCustomer.ACTION_BALANCE_UP,
                                value=d['credit'],
                                action_date=d['action_date'],
                                document_id=d['document_id']
                            )

                            dc.save()
                        else:
                            errors.append({
                                d['document_id']: 'Документ №{} был ранее загружен {}'.format(
                                    d['document_id'], dc.date.date()
                                )
                            })

                elif d['debet'] != '':
                    try:
                        provider = Provider.objects.get(name=d['name'])
                    except dj_exceptions.ObjectDoesNotExist as e:
                        errors.append({d['name']: 'Не удалось найти объект с именем: {}'.format(d['name'])})
                    else:
                        try:
                            dp = DischargeProvider.objects.get(document_id=d['document_id'])
                        except dj_exceptions.ObjectDoesNotExist:
                            success.append(d)
                            dp = DischargeProvider.objects.create(
                                provider=provider,
                                action=DischargeCustomer.ACTION_BALANCE_UP,
                                value=d['debet'],
                                action_date=d['action_date'],
                                document_id=d['document_id']
                            )

                            dp.save()
                        else:
                            errors.append({
                                d['document_id']: 'Документ №{} был ранее загружен {}'.format(
                                    d['document_id'], dp.date.date()
                                )
                            })

            context = {
                 'json': errors + success
            }
            return render(request, 'discharge_app/uploaded.html', context=context)
    else:
        form = UploadFileForm()
    return render(request, 'discharge_app/upload.html', {'form': form})