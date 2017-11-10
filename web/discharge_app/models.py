from django.db import models

from customer_app.models import Customer
from provider_app.models import Provider
from shipment_app.models import Shipment


class DischargeInput(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/', unique_for_date=True)
    date_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(unique_for_date=True)
    json = models.TextField(editable=False, verbose_name="json")

    def file_path(self):
        return self.file.path

    class Meta:
        verbose_name = "Выписка Банка"
        verbose_name_plural = "Выписки Банка"


class DischargeModel(models.Model):
    ACTION_BALANCE_UP = 1
    ACTION_BALANCE_DOWN = 0

    action_choice = (
        (ACTION_BALANCE_UP, 'Пополнение'),
        (ACTION_BALANCE_DOWN, 'Снятие'),
    )

    action = models.IntegerField(choices=action_choice, verbose_name='Операция')
    action_date = models.CharField(max_length=20, verbose_name='Дата операции', blank=True, default=None)
    document_id = models.IntegerField(verbose_name='№ документа', unique=True, blank=True, default=None)
    shipment_id = models.ForeignKey(Shipment, verbose_name='№ отгрузки', blank=True, null=True, default=None)

    value = models.FloatField(verbose_name='Сумма')

    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        abstract = True


class DischargeProvider(DischargeModel, models.Model):
    provider = models.ForeignKey(Provider)

    class Meta:
        verbose_name = "Выписка поставщика"
        verbose_name_plural = "Выписки поставщика"

    def save(self, *args, **kwargs):

        balance = self.provider.saldo_debet - self.provider.saldo_credit
        for discharge in DischargeProvider.objects.filter(provider_id=self.provider_id):
            if discharge.action == self.ACTION_BALANCE_UP:
                balance += discharge.value
            else:
                balance -= discharge.value
        p = Provider.objects.get(pk=self.provider_id)
        p.balance = balance
        p.save()

        super(DischargeProvider, self).save(*args, **kwargs)


class DischargeCustomer(DischargeModel, models.Model):
    customer = models.ForeignKey(Customer)

    class Meta:
        verbose_name = "Выписка заказчика"
        verbose_name_plural = "Выписки заказчика"

    def save(self, *args, **kwargs):

        balance = self.provider.saldo_credit - self.provider.saldo_debet
        for discharge in DischargeCustomer.objects.filter(customer_id=self.customer_id):
            if discharge.action == self.ACTION_BALANCE_UP:
                balance += discharge.value
            else:
                balance -= discharge.value
        p = Customer.objects.get(pk=self.customer_id)
        p.balance = balance
        p.save()

        super(DischargeCustomer, self).save(*args, **kwargs)