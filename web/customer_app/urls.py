from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import CustomerDetailView
from .views import customers

# from .views import filters_views
# from .views import search_views

urlpatterns = [
    url(r'^list/$', login_required(customers), name='customer_list'),
    url(r'^detail/(?P<pk>[0-9]+)/$', login_required(CustomerDetailView.as_view()), name='customer_detail'),

    #url(r'^search/$', search_views.order_search_form, name='customer_search_form'),
    #url(r'^filter$', filters_views.orders_filter, name='customer_filter_views'),
]
