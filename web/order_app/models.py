from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User


from provider_app.models import Provider, Product


class Order(models.Model):
    status_choice = (
        ('CRTD', 'Создан'),
        ('CMPLTD', 'Обработан'),
    )

    receipt_choice = (
        (2, 'Круглосуточно'),
        (0, 'День'),
        (1, 'Ночь'),
    )

    tonar_choice = (
        (1, 'Да'),
        (0, 'Нет'),
    )

    payment_choice = (
        (0, 'Безналичный'),
        (1, 'Наличный'),
    )

    product = models.ForeignKey(Product, default=1)

    # author = models.ForeignKey(User, default=User.objects.get(username='panagoa').pk)
    manager = models.ForeignKey(User)

    volume = models.IntegerField(default=10, verbose_name='Объем')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    status = models.CharField(max_length=7, choices=status_choice, default='CRTD', verbose_name='Статус', db_index=True)

    name = models.CharField(max_length=50, verbose_name='Имя')
    phone_number = models.CharField(max_length=60, null=True, verbose_name='Телефон')
    address = models.CharField(max_length=200, null=True, verbose_name='Адрес')
    tonar = models.IntegerField(choices=tonar_choice, default='Нет', verbose_name='Тонары')
    time_of_receipt = models.IntegerField(choices=receipt_choice, default='День', verbose_name='Время приема')
    payment = models.IntegerField(choices=payment_choice, default='Наличный', verbose_name='Расчет')
    cost = models.IntegerField(default=0, verbose_name='Стоимость')

    # time_stat_p = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата принятия')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_index=True)
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', db_index=True)
    time_completed = models.DateTimeField(blank=True, null=True, verbose_name='Дата обработки', db_index=True)

    longitude = models.FloatField(blank=True, null=True, verbose_name='Долгота')
    latitude = models.FloatField(blank=True, null=True, verbose_name='Широта')
    coordinate = models.CharField(blank=True, null=True, max_length=100, verbose_name='Координаты')

    provider = models.ForeignKey(Provider, default=0, verbose_name='Поставщик')

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

        p = Provider.objects.get(pk=self.provider_id)
        p.orders_count = Order.objects.filter(provider_id=self.provider_id).count()
        p.save()

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return '{}\t({})'.format(self.pk, self.product.name)

    def get_absolute_url(self):
        return reverse('order:order_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    order = models.ForeignKey(Order)
    author = models.ForeignKey(User)
    text = models.TextField(max_length=300)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"

    def get_absolute_url(self):
        return reverse('order:order_detail', kwargs={'pk': self.order_id})


class SmsNotify(models.Model):
    order = models.ForeignKey(Order)
    provider = models.ForeignKey(Provider)
    sms_id = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    time_created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "СМС уведомление"
        verbose_name_plural = "СМС уведомления"
