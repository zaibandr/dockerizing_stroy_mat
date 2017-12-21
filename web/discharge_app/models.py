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
        verbose_name = "Файл Выписки Банка"
        verbose_name_plural = "Файлы Выписок Банка"


class Entity(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование', db_index=True)
    inn = models.TextField(verbose_name='ИНН', max_length=20, unique=True, db_index=True, null=True, default=None)

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'

    def __str__(self):
        return self.name


class DischargeEntity(models.Model):
    entity = models.ForeignKey(Entity)
    document_id = models.IntegerField(verbose_name='№ документа', unique=True, blank=True, default=None)

    debet = models.FloatField(verbose_name='Дебет')
    credit = models.FloatField(verbose_name='Кредит')

    action_date = models.CharField(max_length=20, verbose_name='Дата операции', blank=True, default=None)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Выписка Банка'
        verbose_name_plural = 'Выписки Банка'

    def __str__(self):
        return '{} №({})'.format(self.entity.name, self.document_id)


class DischargeModel(models.Model):
    ACTION_BALANCE_UP = 1
    ACTION_BALANCE_DOWN = 0

    action_choice = (
        (ACTION_BALANCE_UP, 'Пополнение'),
        (ACTION_BALANCE_DOWN, 'Снятие'),
    )

    action = models.IntegerField(choices=action_choice, verbose_name='Операция')
    action_date = models.CharField(max_length=20, verbose_name='Дата операции', blank=True, default=None)

    value = models.FloatField(verbose_name='Сумма')

    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        abstract = True


class DischargeProvider(DischargeModel, models.Model):
    provider = models.ForeignKey(Provider)
    shipment_id = models.ForeignKey(Shipment, verbose_name='№ отгрузки', blank=True, null=True, default=None)

    class Meta:
        verbose_name = "Выписка поставщика (расход)"
        verbose_name_plural = "Выписки поставщика (расходы)"

    def __str__(self):
        return 'Выписка {}: {} - {}р ({})'.format(self.shipment_id.provider.name, self.shipment_id, self.value,
                                                  self.action_date)


class DischargeCustomer(DischargeModel, models.Model):
    customer = models.ForeignKey(Customer)
    shipment_id = models.ForeignKey(Shipment, verbose_name='№ отгрузки', blank=True, null=True, default=None)

    class Meta:
        verbose_name = "Выписка заказчика (приход)"
        verbose_name_plural = "Выписки заказчика (приходы)"

    def __str__(self):
        return 'Выписка {}: {} - {}р ({})'.format(self.shipment_id.customer.name, self.shipment_id, self.value,
                                                  self.action_date)

