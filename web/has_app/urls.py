from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required

from .views import filters_views
from .views import search_views
from .views import orders, new_order_form, provider_notify, add_comment_to_order
from .views import OrderDetailView, EditOrder, OrderUpdate
from .views import ProviderDetailView
from .views import new_shipment_form, EditShipment, shipments

import notifications.urls


urlpatterns = [
    url(r'^$', login_required(orders), name='home'),

    url(r'^m/', include([
        url(r'^new_order/$', permission_required('has_app.add_order')(new_order_form), name='new_order_form'),
        url(r'^orders/(?P<pk>[0-9]+)/edit/$', permission_required('has_app.change_order')(EditOrder.as_view()),
            name='order_edit'),
        url(r'^new_shipment/$', permission_required('has_app.add_shipment')(new_shipment_form),
            name='new_shipment_form'),
        url(r'^shipments/(?P<pk>[0-9]+)/edit/$', permission_required('has_app.change_shipment')(EditShipment.as_view()),
            name='shipment_edit'),
    ])),

    url(r'^s/', include([
        url(r'^orders/(?P<pk>[0-9]+)/update/$', permission_required('has_app.change_order')(OrderUpdate.as_view()),
            name='order_update'),
        url(r'^orders/(?P<pk>[0-9]+)/provider_notify/$', provider_notify, name='provider_notify'),
    ])),

    url(r'^providers/(?P<pk>[0-9]+)/$', login_required(ProviderDetailView.as_view()), name='provider-detail'),

    url(r'^orders/$', login_required(orders), name='orders'),
    url(r'^orders/(?P<pk>[0-9]+)/$', login_required(OrderDetailView.as_view()), name='order-detail'),

    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r"^logout/$", auth_views.logout_then_login, name="logout"),

    url(r'^search/$', search_views.order_search_form, name='search_form'),
    url(r'^autocomplete_order_id/$', search_views.autocomplete_order_id, name='autocomplete_order_id'),
    url(r'^autocomplete_order_address/$', search_views.autocomplete_order_address, name='autocomplete_order_address'),


    url(r'^filter$', filters_views.order_filter_list, name='order_filter'),
    url(r'^filterviews$', filters_views.FilteredOrderListView.as_view(), name='order_filter_views'),

    url(r'^shipments/$', login_required(shipments), name='shipments'),
    url(r'^orders/(?P<pk>[0-9]+)/add_comment/$', add_comment_to_order, name='add_comment_to_order'),

    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
