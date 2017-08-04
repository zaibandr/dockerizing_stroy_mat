from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
# from django.contrib.gis.db import models


class Product(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование')

    class Meta:
        verbose_name = "Наименование"
        verbose_name_plural = "Наименования"

    def __str__(self):
        return self.name


# class CartItem(models.Model):
#     product = models.ForeignKey(Product)
#     quantity = models.IntegerField()
#
#     def __str__(self):
#         return '{}\t({})'.format(self.product.name, self.quantity)
#
#
# class Cart(models.Model):
#     items = models.ManyToManyField(CartItem)


class Order(models.Model):
    status_choice = (
        ('CRTD', 'Создан'),
        ('PRCSD', 'В обработке'),
        ('CMPLTD', 'Обработан'),
    )

    receipt_choice = (
        (2, 'Круглосуточно'),
        (0, 'День'),
        (1, 'Ночь'),
    )

    tonar_choice = (
        (1, 'Дa'),
        (0, 'Нет'),
    )

    payment_choice = (
        (0, 'Безналичный'),
        (1, 'Наличный'),
    )

    product = models.ForeignKey(Product, default=1)

    # author = models.ForeignKey(User, default=User.objects.get(username='panagoa').pk)
    manager = models.ForeignKey(User)

    volume = models.IntegerField(default=3, verbose_name='Объем')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    status = models.CharField(max_length=7, choices=status_choice, default='CRTD', verbose_name='Статус')

    name = models.CharField(max_length=50, verbose_name='Имя')
    phone_number = models.CharField(max_length=12, null=True, verbose_name='Телефон')
    address = models.CharField(max_length=200, null=True, verbose_name='Адрес')
    tonar = models.IntegerField(choices=tonar_choice, default='Нет', verbose_name='Тонары')
    time_of_receipt = models.IntegerField(choices=receipt_choice, default='День', verbose_name='Время приема')
    payment = models.IntegerField(choices=payment_choice, default='Наличный', verbose_name='Расчет')
    cost = models.IntegerField(default=0, verbose_name='Стоимость')

    # time_stat_p = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата принятия')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    time_completed = models.DateTimeField(blank=True, null=True, verbose_name='Дата обработки')

    longitude = models.FloatField(blank=True, null=True, verbose_name='Долгота')
    latitude = models.FloatField(blank=True, null=True, verbose_name='Широта')
    coordinate = models.CharField(blank=True, null=True, max_length=100, verbose_name='Координаты')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def save(self, *args, **kwargs):
        from geopy.geocoders import Yandex

        geo_locator = Yandex()
        location = geo_locator.geocode(self.address, timeout=10)
        self.longitude = location.longitude
        self.latitude = location.latitude
        self.coordinate = location.point

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return '{}\t({})'.format(self.product.name, str(self.time_created))

    def get_absolute_url(self):
        return reverse('order-detail', kwargs={'pk': self.pk})


class Provider(models.Model):

    name = models.CharField(max_length=50, verbose_name='Имя')
    contact_name = models.TextField(max_length=100, verbose_name='Контактное лицо')
    phone_number = models.CharField(max_length=12, null=True, verbose_name='Телефон')
    products = models.ManyToManyField(Product, verbose_name='Продукция')
    # region = models.PolygonField(verbose_name='Регион')
    geo_json = models.TextField(verbose_name='GeoJson')

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('provider-detail', kwargs={'pk': self.pk})


class Zone(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    polygon = models.TextField(verbose_name='Полигон')

    class Meta:
        verbose_name = 'Зона'
        verbose_name_plural = 'Зоны'

    def __str__(self):
        return self.name
