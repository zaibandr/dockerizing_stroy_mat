from django.db import models
from django.urls import reverse

from product_app.models import ProductGeo
from core.models import BalanceModel, DescriptionModel, MailModel, PhoneNumberModel, ContactNameModel


class ProviderCanDeliveryManager(models.Manager):
    use_for_related_fields = True

    def can_delivery(self, point_longitude: float, point_latitude: float, product_id: int):
        from shapely.geometry import Polygon, Point
        from provider_app.models import Provider

        """TODO optimize with haystack spatial search (polygon)"""
        can_delivery_providers = []
        for provider in Provider.objects.filter(regions__products__id__exact=product_id):
            for region in provider.regions.all():
                polygon = Polygon(region.delivery_region['coordinates'][0])
                if polygon.contains(Point(point_longitude, point_latitude)):
                    can_delivery_providers.append(provider)
        return can_delivery_providers


class Provider(PhoneNumberModel, ContactNameModel, DescriptionModel, BalanceModel, MailModel, models.Model):

    name = models.CharField(max_length=50, verbose_name='Поставщик', db_index=True)

    hidden = models.BooleanField(blank=True, default=False, verbose_name='Скрывать')
    regions = models.ManyToManyField(ProductGeo)

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
