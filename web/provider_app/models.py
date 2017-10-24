from django.urls import reverse
from django.db import models
from djgeojson.fields import PolygonField


class Product(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование', db_index=True)

    class Meta:
        verbose_name = "Наименование"
        verbose_name_plural = "Наименования"
        ordering = ['name']

    def __str__(self):
        return self.name


class Provider(models.Model):

    name = models.CharField(max_length=50, verbose_name='Имя', db_index=True)
    contact_name = models.TextField(max_length=400, verbose_name='Контактное лицо')
    phone_number = models.CharField(max_length=12, null=True, verbose_name='Телефон')
    mail_1 = models.EmailField(blank=True, null=True, verbose_name='mail_1')
    mail_2 = models.EmailField(blank=True, null=True, verbose_name='mail_2')

    products = models.ManyToManyField(Product, verbose_name='Продукция')
    hidden = models.BooleanField(blank=True, default=False, verbose_name='Скрывать поставщика')
    # region = models.PolygonField(verbose_name='Регион')
    geom = PolygonField(default='[]')

    balance = models.IntegerField(editable=False, default=0, verbose_name='Баланс')

    orders_count = models.IntegerField(editable=False, default=0, verbose_name='КЗ', db_index=True)
    shipments_count = models.IntegerField(editable=False, default=0, verbose_name='Количесвто отгрузок', db_index=True)

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['-orders_count', '-shipments_count', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('provider:provider_detail', kwargs={'pk': self.pk})

    def balance_add(self, amount):
        self.balance += int(amount)

    def balance_take_down(self, amount):
        self.balance -= int(amount)
