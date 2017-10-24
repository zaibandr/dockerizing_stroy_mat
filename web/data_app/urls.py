from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
    url(r'^provider_orders', login_required(provider_orders), name='provider_orders'),
    url(r'^orders_per_day', login_required(orders_per_day), name='orders_per_day'),
    url(r'^overage_complete_time', login_required(overage_complete_time), name='overage_complete_time'),
    url(r'^all_order_on_map', login_required(all_order_on_map), name='all_order_on_map'),
    url(r'^get_real_ip', login_required(get_real_ip), name='get_real_ip'),
    url(r'^order_triangle', login_required(order_triangle), name='order_triangle'),

]
