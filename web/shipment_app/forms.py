from django.forms import ModelForm, Textarea, Select, SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget

from shipment_app.models import Shipment


class MySelect(Select):
    def render_option(self, selected_choices, option_value, option_label):
        # look at the original for something to start with
        return '<option value="{}" data-tokens="{}">{}</option>'.format(option_value, str(option_label).lower(), option_label)


class NewShipmentForm(ModelForm):

    class Meta:
        model = Shipment
        fields = [
            'deliver',
            'product', 'customer', 'provider', 'transporter', 'address',
            'volume_m',
            'cost_in', 'cost_out', 'price_delivery'
        ]

        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 4}),
            'product': MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'customer': MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'provider': MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'deliver': SelectDateWidget()
        }


class UpdateShipmentManagerForm(ModelForm):
    class Meta:
        model = Shipment
        fields = [
            'deliver',
            'product', 'customer', 'provider', 'transporter', 'address',
            'volume_m',
            'cost_in', 'cost_out', 'price_delivery'
        ]


class UpdateShipmentSupplierForm(ModelForm):
    class Meta:
        model = Shipment
        fields = [
            'provider',
            'volume_s', 'cost_in', 'cost_out',
            'stamp', 'confidant',
            'price_delivery',
        ]


class UpdateShipmentBookerForm(ModelForm):
    class Meta:
        model = Shipment
        fields = [
            'volume_b',
            'ttn',
            'provider_invoice_number', 'customer_invoice_number',
            'provider_document',
            'customer_document'
        ]
