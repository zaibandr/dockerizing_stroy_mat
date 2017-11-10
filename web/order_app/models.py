from django.db import models
from django.urls import reverse

from core.models import OwnerModel, TimeStampedModel, DeliveryModel
from product_app.models import Product
from provider_app.models import Provider
from .abstract_models import OrderNerudInfo, OrderBaseInfo, PaymentInfo
from .managers import NearSimilarOrderManager


class Order(OwnerModel, PaymentInfo, OrderBaseInfo, OrderNerudInfo, DeliveryModel, TimeStampedModel, models.Model):

    product = models.ForeignKey(Product, default=1)
    provider = models.ForeignKey(Provider, default=0, verbose_name='Поставщик')

    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    name = models.CharField(max_length=50, verbose_name='Имя')
    phone_number = models.CharField(max_length=60, null=True, verbose_name='Телефон')

    time_completed = models.DateTimeField(blank=True, null=True, verbose_name='Дата обработки', db_index=True)

    objects = NearSimilarOrderManager()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def save(self, *args, **kwargs):
        from geopy.geocoders import Yandex

        geo_locator = Yandex()
        location = geo_locator.geocode(self.address, timeout=10)
        if location is None:
            location = geo_locator.geocode('г Москва', timeout=10)
            self.address = "Невозможно найти адрес! Убедитесь что адрес верный и повторите ввод."

        self.longitude = location.longitude
        self.latitude = location.latitude

        # p = Provider.objects.get(pk=self.provider_id)
        # p.orders_count = Order.objects.filter(provider_id=self.provider_id).count()
        # p.save()

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return '{}\t({})'.format(self.pk, self.product.name)

    def get_absolute_url(self):
        return reverse('order:order_detail', kwargs={'pk': self.pk})