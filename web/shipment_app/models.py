from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel, DescriptionModel, DeliveryModel, OwnerModel
from product_app.models import Product
from provider_app.models import Provider
from customer_app.models import Customer


class Shipment(TimeStampedModel, OwnerModel, DescriptionModel, DeliveryModel, models.Model):
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

    stamp = models.NullBooleanField(verbose_name='Штамп/печать')
    confidant = models.CharField(max_length=100, blank=True, null=True, verbose_name='Доверенное лицо')

    status = models.CharField(max_length=7, choices=status_choice, default=STATUS_CREATED, verbose_name='Статус')

    volume = models.IntegerField(default=10, verbose_name='Объем')

    cost_in = models.IntegerField(default=0, verbose_name='Цена (входящая)')
    cost_out = models.IntegerField(default=0, verbose_name='Цена (продажная)')

    price_delivery = models.IntegerField(default=0, verbose_name='Стоймость доставки')
    price_total = models.IntegerField(default=0, editable=False, verbose_name='Общая стоймость')
    profit = models.IntegerField(default=0, editable=False, verbose_name='Прибыль')

    delivered = models.DateTimeField(blank=True, null=True, verbose_name='Дата доставки')
    confirmed = models.DateTimeField(blank=True, null=True, verbose_name='Дата Подтверждения')

    class Meta:
        verbose_name = "Отгрузка"
        verbose_name_plural = "Отгрузки"

    def save(self, *args, **kwargs):
        self.profit = (self.cost_out - self.cost_in) * self.volume
        self.price_total = self.cost_out * self.volume + self.price_delivery

        super(Shipment, self).save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.product.name, self.volume)

    def get_absolute_url(self):
        return reverse('shipment_detail', kwargs={'pk': self.pk})
