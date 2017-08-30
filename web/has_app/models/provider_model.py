from django.urls import reverse
from django.db import models
from djgeojson.fields import PolygonField

from .product_model import Product


class Provider(models.Model):

    name = models.CharField(max_length=50, verbose_name='Имя')
    contact_name = models.TextField(max_length=400, verbose_name='Контактное лицо')
    phone_number = models.CharField(max_length=12, null=True, verbose_name='Телефон')
    mail_1 = models.EmailField(blank=True, null=True, verbose_name='mail_1')
    mail_2 = models.EmailField(blank=True, null=True, verbose_name='mail_2')

    products = models.ManyToManyField(Product, verbose_name='Продукция')
    # region = models.PolygonField(verbose_name='Регион')
    geom = PolygonField(default='[]')

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('provider-detail', kwargs={'pk': self.pk})
