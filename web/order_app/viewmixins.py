from notifications.models import Notification
from comment_app.models import Comment


from provider_app.models import Provider
from .models import Order


class NotificationMixin:
    def get_context_data(self, **kwargs):
        context = super(NotificationMixin, self).get_context_data(**kwargs)
        context['unread_notifications'] = Notification.objects.filter(
            recipient=self.request.user,
            action_object_object_id=self.object.pk,
            unread=True)
        return context


class CommentMixin:
    def get_context_data(self, **kwargs):
        context = super(CommentMixin, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(order=self.object.pk)
        return context


class NotifiedProviderTableMixin:
    def get_context_data(self, **kwargs):
        from smsnotify_app.models import SmsNotify
        from smsnotify_app.tables import NotifiedProviders

        context = super(NotifiedProviderTableMixin, self).get_context_data(**kwargs)
        context['notified_providers'] = NotifiedProviders(
            SmsNotify.objects.filter(order=self.object.pk).select_related('provider')
        )

        return context


class ProviderTableMixin:

    def get_context_data(self, **kwargs):
        from provider_app.tables import AvailableProviderTable

        context = super(ProviderTableMixin, self).get_context_data(**kwargs)
        context['providers_table'] = AvailableProviderTable(
            Provider.objects.can_delivery(self.object.longitude, self.object.latitude, self.object.product_id)
        )
        return context


class NearSimilarMixin:
    def get_similar(self, km=10):
        similar_order = Order.objects.near_similar_order(
            self.object.longitude, self.object.latitude, self.object.product_id,  km=km
        )
        similar_order_pk = [order.pk for order in similar_order]

        similar = Order.objects.filter(
            pk__in=similar_order_pk, status=Order.STATUS_COMPLETED
        ).exclude(pk=self.object.pk).select_related('provider', 'product')

        return similar

    def get_context_data(self, **kwargs):
        from .tables import SimilarOrderTable

        context = super(NearSimilarMixin, self).get_context_data(**kwargs)

        similar_10 = self.get_similar(10)
        similar_20 = self.get_similar(20)

        context['near_similar_order_10_km'] = similar_10
        context['near_similar_order_20_km'] = similar_20

        # context['near_similar_order_10_km_table'] = SimilarOrderTable(similar_10)
        # context['near_similar_order_20_km_table'] = SimilarOrderTable(similar_20)

        return context


class GeoJsonMixin:
    def get_context_data(self, **kwargs):
        from shapely.geometry import Polygon, Point
        import random
        import json

        context = super(GeoJsonMixin, self).get_context_data(**kwargs)

        colors = [
            'Red', 'DarkRed', 'Yellow', 'OrangeRed',
            'Blue', 'DarkBlue', 'DeepSkyBlue', 'DeepPink',
            'Green', 'Lime', 'SpringGreen', 'Black'
        ]

        geo_json = {
            "type": "FeatureCollection",
            "features": []
        }
        providers = Provider.objects.can_delivery(self.object.longitude, self.object.latitude, self.object.product_id)
        for provider in providers:
            color = random.choice(colors)
            for region in provider.regions.filter(products__id__exact=self.object.product_id):
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

        # Сортировка полигонов по площади
        geo_json['features'] = sorted(
            geo_json['features'],
            key=lambda f: Polygon(f['geometry']['coordinates'][0]).area,
            reverse=True
        )

        context['geo_json'] = json.dumps(geo_json)

        return context

