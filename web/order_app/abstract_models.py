from django.db import models


class OrderNerudInfo(models.Model):
    RECEIPT_DAY = 'D'
    RECEIPT_NIGHT = 'N'
    RECEIPT_BOTH = 'B'

    receipt_choice = (
        (RECEIPT_BOTH, 'Круглосуточно'),
        (RECEIPT_DAY, 'День'),
        (RECEIPT_NIGHT, 'Ночь'),
    )

    TONAR_YES = 1
    TONAR_NO = 0

    tonar_choice = (
        (TONAR_YES, 'Да'),
        (TONAR_NO, 'Нет'),
    )

    tonar = models.IntegerField(choices=tonar_choice, default=TONAR_NO, verbose_name='Тонары')
    time_of_receipt = models.CharField(max_length=2, choices=receipt_choice,
                                       default=RECEIPT_BOTH, verbose_name='Время приема')

    class Meta:
        abstract = True


class OrderBaseInfo(models.Model):
    STATUS_CREATED = 'CR'
    STATUS_COMPLETED = 'CM'

    status_choice = (
        (STATUS_CREATED, 'Создан'),
        (STATUS_COMPLETED, 'Обработан'),
    )

    PAYMENT_CASH = 1
    PAYMENT_NON_CASH = 0

    payment_choice = (
        (PAYMENT_NON_CASH, 'Безналичный'),
        (PAYMENT_CASH, 'Наличный'),
    )

    status = models.CharField(max_length=7, choices=status_choice, default='CRTD', verbose_name='Статус', db_index=True)
    volume = models.IntegerField(default=10, verbose_name='Объем')
    payment = models.IntegerField(choices=payment_choice, default='Наличный', verbose_name='Расчет')

    class Meta:
        abstract = True

    # def geo_data(order):
    #
    #     import random
    #
    #     point_within_provider = []
    #     geo_data = []
    #
    #     for provider in Provider.objects.filter(products__id__exact=order.product.id):
    #         polygon = Polygon(provider.geom['coordinates'][0])
    #         if polygon.contains(Point(order.longitude, order.latitude)):
    #             point_within_provider.append(provider.pk)
    #
    #             color = random.choice(
    #                 [
    #                     'Red', 'DarkRed', 'Yellow', 'OrangeRed',
    #                     'Blue', 'DarkBlue', 'DeepSkyBlue', 'DeepPink',
    #                     'Green', 'Lime', 'SpringGreen', 'Black'
    #                 ]
    #             )
    #             popup = '<a href="{}" >{}</a>'.format(provider.get_absolute_url(), provider.name)
    #             poly_coords = [[p[1], p[0]] for p in provider.geom['coordinates'][0]]
    #             name = 'provider_{}'.format(str(provider.pk))
    #
    #             geo_data.append([polygon, name, popup, poly_coords, color])
    #
    #     sorted_geo_data = sorted(geo_data, key=lambda a: a[0].area, reverse=True)
    #
    #     geo_data = [[name, popup, poly_coords, color] for _, name, popup, poly_coords, color in sorted_geo_data]
    #
    #     return point_within_provider, geo_data


class DeliveryInfo(models.Model):
    address = models.CharField(max_length=200, null=True, verbose_name='Адрес', )
    longitude = models.FloatField(blank=True, null=True, verbose_name='Долгота')
    latitude = models.FloatField(blank=True, null=True, verbose_name='Широта')
    coordinate = models.CharField(blank=True, null=True, max_length=100, verbose_name='Координаты')

    class Meta:
        abstract = True


class PaymentInfo(models.Model):
    cost = models.IntegerField(default=0, verbose_name='Стоимость')
    pick_cost = models.IntegerField(default=0, verbose_name='Стоимость самовывоза')
    delivery_cost = models.IntegerField(default=0, verbose_name='Стоимость c доставкой')

    class Meta:
        abstract = True