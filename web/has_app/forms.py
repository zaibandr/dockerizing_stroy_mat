from django.forms import ModelForm, Textarea, HiddenInput, Select
from .models import Order


class MySelect(Select):
    def render_option(self, selected_choices, option_value, option_label):
        # look at the original for something to start with
        return '<option value="{}" data-tokens="{}">{}</option>'.format(option_value, str(option_label).lower(), option_label)


class NewOrderForm(ModelForm):
    class Meta:
        model = Order
        # fields = ['product', 'volume', 'description', 'status', 'phone_number', 'address', 'time_stat_p']
        fields = ['product', 'manager', 'address', 'name', 'phone_number', 'volume', 'description', 'status', 'tonar', 'time_of_receipt', 'payment']
        exclude = ['manager', 'status']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 4}),
            'product': MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'})

        }


class EditOrderForm(ModelForm):
    class Meta:
        model = Order
        # fields = ['product', 'volume', 'description', 'status', 'phone_number', 'address', 'time_stat_p']
        fields = ['product', 'manager', 'address', 'name', 'phone_number', 'volume', 'description', 'status', 'tonar', 'time_of_receipt', 'payment']
        exclude = ['manager', 'status']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 4}),
            'product': MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'})

        }


class UpdateOrderForm(ModelForm):
    class Meta:
        model = Order

        fields = ['cost', 'status', 'time_completed']
        widgets = {'time_completed': HiddenInput()}
