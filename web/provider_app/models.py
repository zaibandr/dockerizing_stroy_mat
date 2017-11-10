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
        for provider in Provider.objects.filter(regions__products__id__exact=product_id).prefetch_related('regions'):
            for region in provider.regions.all():
                polygon = Polygon(region.delivery_region['coordinates'][0])
                if polygon.contains(Point(point_longitude, point_latitude)):
                    can_delivery_providers.append(provider.pk)
        return Provider.objects.filter(pk__in=can_delivery_providers)


class Provider(PhoneNumberModel, ContactNameModel, DescriptionModel, BalanceModel, MailModel, models.Model):

    name = models.CharField(max_length=50, verbose_name='Поставщик', db_index=True)

    hidden = models.BooleanField(blank=True, default=False, verbose_name='Скрывать')
    regions = models.ManyToManyField(Region, blank=True, verbose_name='Регион поставок')
    pick_points = models.ManyToManyField(PickPoint, blank=True, verbose_name='Точки самовывоза')

    orders_count = models.IntegerField(editable=False, default=0, verbose_name='КЗ', db_index=True)
    shipments_count = models.IntegerField(editable=False, default=0, verbose_name='Количесвто отгрузок', db_index=True)

    objects = ProviderCanDeliveryManager()

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['-orders_count', '-shipments_count', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('provider:provider_detail', kwargs={'pk': self.pk})
