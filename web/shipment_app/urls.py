from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required

from .views import new_shipment_form, EditShipment, shipments, ShipmentDetailView

urlpatterns = [
    url(r'^list/$', login_required(shipments), name='shipments_list'),
    url(r'^new/$', new_shipment_form, name='new_shipment_form'),

    url(r'^detail/(?P<pk>[0-9]+)/$', login_required(ShipmentDetailView.as_view()), name='shipment_detail'),
    url(r'^edit/(?P<pk>[0-9]+)/$', EditShipment.as_view(), name='shipment_edit'),
]
