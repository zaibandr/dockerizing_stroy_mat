from notifications.models import Notification
from comment_app.models import Comment

import random
from shapely.geometry import Polygon, Point

from provider_app.models import Provider


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


class PolygonDrawMixin:
    def get_context_data(self, **kwargs):
        context = super(PolygonDrawMixin, self).get_context_data(**kwargs)


class NotifiedProviderTableMixin:
    def get_context_data(self, **kwargs):
        from smsnotify_app.models import SmsNotify
        from smsnotify_app.tables import NotifiedProviders

        context = super(NotifiedProviderTableMixin, self).get_context_data(**kwargs)
        context['notified_providers'] = NotifiedProviders(SmsNotify.objects.filter(order=self.object.pk))

        return context


class ProviderTableMixin:

    def get_context_data(self, **kwargs):
        from provider_app.tables import AvailableProviderTable

        context = super(ProviderTableMixin, self).get_context_data(**kwargs)
        context['providers_table'] = AvailableProviderTable(
            Provider.objects.can_delivery(self.object.longitude, self.object.latitude, self.object.product_id)
        )
        return context

