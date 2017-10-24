from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required, permission_required

from .views import filters_views
from .views import search_views
from .views import orders, new_order_form, provider_notify, notify_cost, multi_order_create, new_order_with_formset
from .views import OrderDetailView, EditOrder, OrderUpdate
from .views import add_comment_to_order, EditComment

urlpatterns = [
    url(r'^m/', include([
        url(r'^new/$', permission_required('order_app.add_order')(new_order_form), name='new_order_form'),
        url(r'^new_formset/$', permission_required('order_app.add_order')(new_order_with_formset), name='new_order_formset'),
        url(r'^edit/(?P<pk>[0-9]+)$', permission_required('order_app.change_order')(EditOrder.as_view()),
            name='order_edit'),
    ])),

    url(r'^s/', include([
        url(r'^update/(?P<pk>[0-9]+)$', permission_required('order.change_order')(OrderUpdate.as_view()),
            name='order_update'),
        url(r'^provider_notify/(?P<pk>[0-9]+)/$', provider_notify, name='provider_notify'),
        url(r'^notify_cost/(?P<pk>[0-9]+)/$', notify_cost, name='notify_cost'),
    ])),

    url(r'^list/$', login_required(orders), name='order_list'),
    url(r'^detail/(?P<pk>[0-9]+)/$', login_required(OrderDetailView.as_view()), name='order_detail'),

    url(r'^search/$', search_views.order_search_form, name='order_search_form'),

    url(r'^autocomplete_id/$', search_views.autocomplete_order_id, name='autocomplete_order_id'),
    url(r'^autocomplete_address/$', search_views.autocomplete_order_address, name='autocomplete_order_address'),


    url(r'^filter$', filters_views.orders_filter, name='order_filter_views'),

    url(r'^add_comment/(?P<pk>[0-9]+)/$', add_comment_to_order, name='add_comment_to_order'),
    url(r'^edit_comment/(?P<pk>[0-9]+)/$', EditComment.as_view(), name='edit_comment'),

    # url(r'^new_multi_order/$', permission_required('has_app.add_order')(multi_order_create), name='new_order_form'),
]
