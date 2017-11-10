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

    TONAR_YES = 't'
    TONAR_NO = 'f'

    tonar_choice = (
        (TONAR_YES, 'Да'),
        (TONAR_NO, 'Нет'),
    )

    tonar = models.CharField(max_length=2, choices=tonar_choice, default=TONAR_YES, verbose_name='Тонары')
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

    PAYMENT_CASH = 't'
    PAYMENT_NON_CASH = 'f'

    payment_choice = (
        (PAYMENT_NON_CASH, 'Безналичный'),
        (PAYMENT_CASH, 'Наличный'),
    )

    status = models.CharField(max_length=7, choices=status_choice, default=STATUS_CREATED, verbose_name='Статус', db_index=True)
    volume = models.IntegerField(default=10, verbose_name='Объем')
    payment = models.CharField(max_length=2, choices=payment_choice, default=PAYMENT_NON_CASH, verbose_name='Расчет')

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


class PaymentInfo(models.Model):
    cost = models.IntegerField(default=0, null=True, blank=True, verbose_name='Стоимость')
    pick_cost = models.IntegerField(default=0, null=True, blank=True,  verbose_name='Стоимость самовывоза')
    delivery_cost = models.IntegerField(default=0, null=True, blank=True, verbose_name='Стоимость c доставкой')

    class Meta:
        abstract = True