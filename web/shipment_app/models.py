from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

from order_app.models import Product
from provider_app.models import Provider


class Shipment(models.Model):
    status_choice = (
        ('CRTD', 'Создан'),
        ('PRCSG', 'На отгрузке'),
        ('CMPLTD', 'Отгружено'),
    )

    product = models.ForeignKey(Product, default=1)
    status = models.CharField(max_length=7, choices=status_choice, default='CRTD', verbose_name='Статус')
    customer = models.CharField(max_length=100, verbose_name='Покупатель')
    provider = models.ForeignKey(Provider, default=0, verbose_name='Поставщик')
    transporter = models.CharField(max_length=100, verbose_name='Перевозчик')
    address = models.CharField(max_length=200, null=True, verbose_name='Адрес')

    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    manager = models.ForeignKey(User)

    volume = models.IntegerField(default=10, verbose_name='Объем')

    cost_in = models.IntegerField(default=0, verbose_name='Стоимость (входящая)')
    cost_out = models.IntegerField(default=0, verbose_name='Стоимость (продажная)')

    price = models.IntegerField(default=0, editable=False, verbose_name='Цена')
    profit = models.IntegerField(default=0, editable=False, verbose_name='Прибыль')

    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    time_completed = models.DateTimeField(blank=True, null=True, verbose_name='Дата обработки')

    class Meta:
        verbose_name = "Отгрузка"
        verbose_name_plural = "Отгрузки"

    def save(self, *args, **kwargs):
        self.profit = (self.cost_out - self.cost_in) * self.volume
        self.price = self.cost_out * self.volume

        super(Shipment, self).save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.product.name, self.volume)

    def get_absolute_url(self):
        return reverse('shipment_detail', kwargs={'pk': self.pk})
