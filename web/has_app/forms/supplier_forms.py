from django.forms import ModelForm, HiddenInput
from has_app.models import Order
from has_app.forms import MySelect


class UpdateOrderForm(ModelForm):
    class Meta:
        model = Order

        fields = ['provider', 'cost', 'status', 'time_completed']
        widgets = {
            'time_completed': HiddenInput(),
            'status': HiddenInput(),
            'provider': MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
        }
