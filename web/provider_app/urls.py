from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import ProviderDetailView, FilteredProviderListView, provider_list

urlpatterns = [
    url(r'^list/$', login_required(provider_list), name='provider_list'),
    url(r'^detail/(?P<pk>[0-9]+)/$', login_required(ProviderDetailView.as_view()), name='provider_detail'),
    url(r'^filter$', FilteredProviderListView.as_view(), name='provider_filter'),
]
