from django.forms import ModelForm, Textarea, Select

from shipment_app.models import Shipment


class MySelect(Select):
    def render_option(self, selected_choices, option_value, option_label):
        # look at the original for something to start with
        return '<option value="{}" data-tokens="{}">{}</option>'.format(option_value, str(option_label).lower(), option_label)


class NewShipmentForm(ModelForm):

    class Meta:
        model = Shipment
        fields = [
            'product',
            'customer',
            'provider',
            'transporter',
            'address',

            'description',
            'manager',

            'volume',
            'cost_in',
            'cost_out',


            'manager',
            'status',
            'price',
            'profit'
        ]

        exclude = ['manager', 'status', 'price', 'profit']

        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 4}),
            'product': MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
        }


class EditShipmentForm(NewShipmentForm):
    pass