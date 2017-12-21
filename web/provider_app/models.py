from django.db import models
from django.urls import reverse

from product_app.models import Region, PickPoint
from core.models import BalanceModel, DescriptionModel, MailModel, PhoneNumberModel, ContactNameModel


class ProviderCanDeliveryManager(models.Manager):
    use_for_related_fields = True

    def can_delivery(self, point_longitude: float, point_latitude: float, product_id: int):
        from shapely.geometry import Polygon, Point
        from provider_app.models import Provider

        """TODO optimize with haystack spatial search (polygon)"""
        can_delivery_providers = []
        # for provider in Provider.objects.filter(
        #         regions__products__id__exact=product_id).prefetch_related('regions', 'regions__products'):
        for region in Region.objects.filter(products__exact=product_id):
            polygon = Polygon(region.delivery_region['coordinates'][0])
            if polygon.contains(Point(point_longitude, point_latitude)):
                can_delivery_providers.append(region.pk)
        return Provider.objects.filter(regions__in=set(can_delivery_providers))


class Provider(PhoneNumberModel, ContactNameModel, DescriptionModel, BalanceModel, MailModel, models.Model):

    name = models.CharField(max_length=200, verbose_name='Поставщик', db_index=True)
    inn = models.CharField(verbose_name='ИНН', max_length=20, unique=True, db_index=True, null=True, default=None)

    hidden = models.BooleanField(blank=True, default=False, verbose_name='Скрывать')
    regions = models.ManyToManyField(Region, blank=True, verbose_name='Регион поставок')
    pick_points = models.ManyToManyField(PickPoint, blank=True, verbose_name='Точка самовывоза')

    orders_count = models.IntegerField(editable=False, default=0, verbose_name='КЗ', db_index=True)
    shipments_count = models.IntegerField(editable=False, default=0, verbose_name='Количесвто отгрузок', db_index=True)

    objects = ProviderCanDeliveryManager()

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['-orders_count', '-shipments_count', 'name']

    # def save(self, *args, **kwargs):
    #
    #     balance = self.saldo_credit - self.saldo_debet
    #     for discharge in DischargeProvider.objects.filter(provider_id=self.pk):
    #         if discharge.action == DischargeProvider.ACTION_BALANCE_UP:
    #             balance += discharge.value
    #         else:
    #             balance -= discharge.value
    #
    #     self.balance = balance
    #
    #     super(Provider, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('provider:provider_detail', kwargs={'pk': self.pk})
