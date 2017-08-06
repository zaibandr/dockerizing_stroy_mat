from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required

from . import views
from . import search_views

urlpatterns = [
    url(r'^$', login_required(views.orders), name='home'),
    url(r'^new_order/$', permission_required('has_app.add_order')(views.new_order_form), name='new_order_form'),
    # url(r'^order_create/$', permission_required('has_app.add_order')(views.OrderCreate.as_view()), name='order_create'),
    url(r'^orders/$', login_required(views.orders), name='orders'),
    url(r'^orders/(?P<pk>[0-9]+)/$', login_required(views.OrderDetailView.as_view()), name='order-detail'),
    url(r'^orders/(?P<pk>[0-9]+)/edit/$', permission_required('has_app.change_order')(views.EditOrder.as_view()),
        name='order_edit'),
    url(r'^orders/(?P<pk>[0-9]+)/update/$', permission_required('has_app.change_order')(views.OrderUpdate.as_view()),
        name='order_update'),
    url(r'^accounts/login/$', auth_views.login, name='login'),

    # url(r'^logout/$', auth_views.logout, name='logout'),
    url(r"^logout/$", auth_views.logout_then_login, name="logout"),

    url(r'^search/$', search_views.order_search_form, name='search_form'),
    url(r'^autocomplete/$', search_views.autocomplete, name='autocomplete'),
]
