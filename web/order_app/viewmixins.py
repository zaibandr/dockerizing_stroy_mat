from notifications.models import Notification
from comment_app.models import Comment


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
        context['providers_table'] = AvailableProviderTable(self.object.can_delivery_providers())
        return context


class NearSimilarMixin:
    def get_context_data(self, **kwargs):
        from .tables import SimilarOrderTable

        context = super(NearSimilarMixin, self).get_context_data(**kwargs)

        similar_10 = self.object.near_similar_order(km=10).select_related('provider', 'product')
        similar_20 = self.object.near_similar_order(km=20).select_related('provider', 'product')

        context['near_similar_order_10_km'] = similar_10
        context['near_similar_order_20_km'] = similar_20

        # context['near_similar_order_10_km_table'] = SimilarOrderTable(similar_10)
        # context['near_similar_order_20_km_table'] = SimilarOrderTable(similar_20)

        return context


class GeoJsonMixin:
    def get_context_data(self, **kwargs):
        from shapely.geometry import Polygon, Point
        import json

        context = super(GeoJsonMixin, self).get_context_data(**kwargs)

        geo_json = self.object.get_geo_json

        # Сортировка полигонов по площади
        geo_json['features'] = sorted(
            geo_json['features'],
            key=lambda f: Polygon(f['geometry']['coordinates'][0]).area,
            reverse=True
        )

        context['geo_json'] = json.dumps(geo_json)

        return context

