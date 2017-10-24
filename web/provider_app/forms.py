

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