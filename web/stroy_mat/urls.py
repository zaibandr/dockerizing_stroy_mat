import notifications.urls
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from order_app.views import orders
from .settings import Prod

urlpatterns = [
    # url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r"^logout/$", auth_views.logout_then_login, name="logout"),
    # url(r'^', include('has_app.urls')),

    url(r'^$', orders, name='main'),

    url(r'^provider/', include('provider_app.urls', namespace='provider', app_name='provider_app'), name='provider'),
    url(r'^customer/', include('customer_app.urls', namespace='customer', app_name='customer_app'), name='customer'),

    url(r'^order/', include('order_app.urls', namespace='order', app_name='order_app'), name='order'),
    url(r'^shipment/', include('shipment_app.urls', namespace='shipment', app_name='shipment_app'), name='shipment'),

    url(r'^data/', include('data_app.urls', namespace='data', app_name='data_app'), name='data'),
    url(r'^discharge/', include('discharge_app.urls', namespace='discharge', app_name='discharge_app')),

    url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^comments/', include('comment_app.urls', namespace='comments')),
]

if 'debug_toolbar' in Prod.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]