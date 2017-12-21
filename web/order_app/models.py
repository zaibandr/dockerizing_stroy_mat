from django.db import models
from django.urls import reverse
from cacheops import cached

from core.models import OwnerModel, TimeStampedModel, DeliveryModel, AttributesModel
from product_app.models import Product
from provider_app.models import Provider
from .abstract_models import OrderNerudInfo, OrderBaseInfo, PaymentInfo
from .managers import NearSimilarOrderManager


class Order(OwnerModel, PaymentInfo, OrderBaseInfo, OrderNerudInfo, DeliveryModel, TimeStampedModel,
            AttributesModel,
            models.Model):

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

    def can_delivery_providers(self):
        from shapely.geometry import Polygon, Point
        from provider_app.models import Provider
        from product_app.models import Region

        """TODO optimize with haystack spatial search (polygon)"""
        within_regions = []
        for region in Region.objects.filter(products__exact=self.product_id):
            polygon = Polygon(region.delivery_region['coordinates'][0])
            if polygon.contains(Point(self.longitude, self.latitude)):
                within_regions.append(region.pk)

        providers_pk = Provider.objects.filter(regions__in=within_regions).values('pk').distinct()
        return Provider.objects.filter(pk__in=providers_pk)

    def near_similar_order(self, km: int=10):
        from haystack.query import SearchQuerySet
        from haystack.utils.geo import Point, D
        point = Point(self.longitude, self.latitude)

        sqs = SearchQuerySet().filter(product=self.product_id).dwithin(
            'location',
            point,
            D(km=km)
        ).distance('location', point).order_by('distance')

        similar = Order.objects.filter(
            pk__in=[o.pk for o in sqs], status=Order.STATUS_COMPLETED
        ).exclude(pk=self.pk)

        return similar

    @property
    def get_geo_json(self):
        @cached(timeout=60 * 60 * 2, extra=self.pk)
        def _geo_json():

            import random

            colors = [
                'Red', 'DarkRed', 'Yellow', 'OrangeRed',
                'Blue', 'DarkBlue', 'DeepSkyBlue', 'DeepPink',
                'Green', 'Lime', 'SpringGreen', 'Black'
            ]

            geo_json = {
                "type": "FeatureCollection",
                "features": []
            }

            for provider in self.can_delivery_providers():
                color = random.choice(colors)
                for region in provider.regions.filter(products__id__exact=self.product_id):
                    feature = {
                        "type": "Feature",
                        "properties": {
                            "popup": '<a href="{}" >{}</a>'.format(provider.get_absolute_url(), provider.name),
                            "color": color,
                            "fillColor": color,
                            "fillOpacity": 0
                        },
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": region.delivery_region['coordinates']
                        }
                    }

                    geo_json['features'].append(feature)

            return geo_json

        return _geo_json()

    @property
    def popup(self):
        from django.utils.html import format_html

        @cached(timeout=60 * 60 * 2, extra=self.pk)
        def _build_popup():
            from core.utils import url_params_create
            return format_html(
                '<a href="{order_url}" title="Перейти на страницу заказа №{order_pk}">{address}</a>  '
                '<a href="{filter_url}" role="button" target="_blank" title="Показать все заказы по этому адресу" class="btn btn-default btn-xs">'
                '<span class="glyphicon glyphicon-search" aria-hidden="true"></span>'
                '</a>'
                '<hr>'
                '{product_name} - '
                '<a href="{provider_url}" title="Перейти на страницу поставщика ">{provider_name}</a>'
                '<hr>'
                'Объем: {volume} - {cost}р',
                order_url=self.get_absolute_url(),
                order_pk=self.pk,
                address=self.address,
                filter_url=reverse('order:order_filter_views')+url_params_create(address=self.address),
                product_name=self.product.name,
                provider_url=self.provider.get_absolute_url(),
                provider_name=self.provider.name,
                volume=self.volume,
                cost=self.cost
            )
        return _build_popup

    def save(self, *args, **kwargs):
        self._address_prepare()

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return '{}\t({})'.format(self.pk, self.product.name)

    def get_absolute_url(self):
        return reverse('order:order_detail', kwargs={'pk': self.pk})