from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel, DescriptionModel, DeliveryModel, OwnerModel
from customer_app.models import Customer
from product_app.models import Product
from provider_app.models import Provider


class BookerAbstract(models.Model):
    volume_b = models.IntegerField(default=0, verbose_name='Объем (Б)')  # Бухгалтер

    ttn = models.NullBooleanField(verbose_name='Наличие транспортной накладной')

    provider_invoice_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        default='',
        verbose_name='Номер счет-фактуры поставшика'
    )

    customer_invoice_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        default='',
        verbose_name='Номер счет-фактуры заказчика'
    )

    DOCUMENTS_YES = 'Y'
    DOCUMENTS_NO = 'N'
    DOCUMENTS_SCAN = 'S'

    document_choice = (
        (DOCUMENTS_YES, 'Есть'),
        (DOCUMENTS_NO, 'Нет'),
        (DOCUMENTS_NO, 'Скан')
    )

    provider_document = models.CharField(
        max_length=4,
        choices=document_choice,
        default=DOCUMENTS_NO,
        verbose_name='Документы от поставщика'
    )

    customer_document = models.CharField(
        max_length=4,
        choices=document_choice,
        default=DOCUMENTS_NO,
        verbose_name='Документы от заказчика'
    )

    class Meta:
        abstract = True


class ManagerAbstract(models.Model):

    volume_m = models.IntegerField(default=10, verbose_name='Объем (М)')  # Менеджер
    cost_out = models.IntegerField(default=0, verbose_name='Цена (продажная)')

    class Meta:
        abstract = True


class SupplierAbstract(models.Model):
    volume_s = models.IntegerField(default=0, verbose_name='Объем (С)')  # Снабженец
    cost_in = models.IntegerField(default=0, verbose_name='Цена (входящая)')
    price_delivery = models.IntegerField(default=0, verbose_name='Стоймость доставки')

    stamp = models.NullBooleanField(verbose_name='Штамп/печать')
    confidant = models.CharField(max_length=100, blank=True, null=True, verbose_name='Доверенное лицо')

    class Meta:
        abstract = True


class Shipment(ManagerAbstract, SupplierAbstract, BookerAbstract, TimeStampedModel, OwnerModel,
               DescriptionModel, DeliveryModel, models.Model):

    STATUS_CREATED = 'CR'
    STATUS_DELIVERED = 'DL'
    STATUS_CONFIRMED = 'CN'

    status_choice = (
        (STATUS_CREATED, 'Создан'),
        (STATUS_DELIVERED, 'Доставлен'),
        (STATUS_CONFIRMED, 'Подтвержден'),
    )

    product = models.ForeignKey(Product, default=1)
    customer = models.ForeignKey(Customer, verbose_name='Покупатель')
    provider = models.ForeignKey(Provider, default=0, verbose_name='Поставщик')
    transporter = models.CharField(max_length=100, blank=True, null=True, verbose_name='Перевозчик')

    payment = models.CharField(max_length=50, blank=True, null=True, verbose_name='Основание оплаты')

    confirmed = models.DateField(blank=True, null=True, verbose_name='Дата Подтверждения')
    deliver = models.DateField(blank=True, null=True, verbose_name='Дата доставки')

    # auto fields
    status = models.CharField(max_length=7, choices=status_choice, default=STATUS_CREATED, verbose_name='Статус')
    price_total = models.IntegerField(default=0, editable=False, verbose_name='Общая стоймость')
    profit = models.IntegerField(default=0, editable=False, verbose_name='Прибыль')

    class Meta:
        verbose_name = "Отгрузка"
        verbose_name_plural = "Отгрузки"

    def _price_calculate(self):
        volume = self.volume_m
        if self.volume_m == self.volume_s == self.volume_b:
            self.status = self.STATUS_CONFIRMED
        elif self.volume_s > 0:
            self.status = self.STATUS_DELIVERED
            volume = self.volume_s
        else:
            self.status = self.STATUS_CREATED

        self.profit = (self.cost_out - self.cost_in) * volume
        self.price_total = self.cost_out * volume  # + self.price_delivery

    def get_data_json(self):
        data = []
        for field in self._meta.get_fields():
            try:
                data.append((field.verbose_name, getattr(self, field.name, None)))
            except AttributeError:
                data.append((field.name, getattr(self, field.name, None)))

        return data

    def save(self, *args, **kwargs):
        self._price_calculate()
        self._address_prepare()

        super(Shipment, self).save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.product.name, self.volume_m)

    def get_absolute_url(self):
        #return reverse('shipment_detail', kwargs={'pk': self.pk})
        return reverse('shipment:shipments_list')