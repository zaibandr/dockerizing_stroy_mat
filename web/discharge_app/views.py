import django.core.exceptions as dj_exceptions
from django.shortcuts import render
from .forms import UploadFileForm
from .models import DischargeInput, DischargeCustomer
from customer_app.models import Customer

from .excel.excel_import import discharge_excel_to_json
import json
import datetime


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if len(DischargeInput.objects.filter(date=datetime.datetime.now().date())) != 0:
                context = {'json': {'error': 'Сегодня уже была загружена выписка'}}

                return render(request, 'discharge_app/uploaded.html', context=context)

            instance = DischargeInput(file=request.FILES['file'])
            instance.date = datetime.datetime.now().date()
            instance.save()

            latest_upload = DischargeInput.objects.last()

            data = json.loads(discharge_excel_to_json(latest_upload.file.path))

            try:
                for d in data:
                    if d['credit'] != '':
                        customer = Customer.objects.get(name=d['name'])
            except dj_exceptions.ObjectDoesNotExist:
                latest_upload.delete()

                context = {'json': {'error': 'Не удалось найти объект с именем: {}'.format(d['name'])}}

                return render(request, 'discharge_app/uploaded.html', context=context)
            else:
                for d in data:
                    if d['credit'] != '':
                        customer = Customer.objects.get(name=d['name'])

                        dc = DischargeCustomer.objects.create(
                            customer=customer,
                            action=1, value=d['credit']
                        )
                        dc.save()

            context = {
                 'json': data
            }
            return render(request, 'discharge_app/uploaded.html', context=context)
    else:
        form = UploadFileForm()
    return render(request, 'discharge_app/upload.html', {'form': form})