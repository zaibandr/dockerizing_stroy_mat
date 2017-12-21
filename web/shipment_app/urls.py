from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import new_shipment_form, ShipmentAdd, EditShipment, shipments, ShipmentDetailView, ShipmentList

urlpatterns = [
    url(r'^list/$', ShipmentList.as_view(), name='shipments_list'),
    url(r'^new/$', login_required(ShipmentAdd.as_view()), name='new_shipment_form'),
    url(r'^add/$', login_required(ShipmentAdd.as_view()), name='shipment_add'),

    url(r'^detail/(?P<pk>[0-9]+)/$', login_required(ShipmentDetailView.as_view()), name='shipment_detail'),
    url(r'^edit/(?P<pk>[0-9]+)/$', login_required(EditShipment.as_view()), name='shipment_edit'),
]
