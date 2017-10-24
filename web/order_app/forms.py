from django.forms import ModelForm, Textarea, Select, ModelChoiceField, IntegerField, HiddenInput, Form
from haystack.forms import SearchForm

from .models import Order, Product, Comment


class MySelect(Select):
    def render_option(self, selected_choices, option_value, option_label):
        # look at the original for something to start with
        return '<option value="{}" data-tokens="{}">{}</option>'.format(option_value, str(option_label).lower(), option_label)


class OrderFormSet(Form):
    product = ModelChoiceField(label='Наименование',
                               queryset=Product.objects.all(),
                               required=True,
                               widget=MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
                               )
    volume = IntegerField(label='Объем')


class MultiOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['manager', 'address', 'name',
                  'phone_number', 'description',
                  'status', 'tonar', 'time_of_receipt', 'payment',
                  'longitude', 'latitude', 'coordinate'
                  ]

        exclude = ['manager', 'status', 'longitude', 'latitude', 'coordinate']

        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 4}),
        }


class NewOrderForm(ModelForm):
    # product = ModelChoiceField(
    #     required=False,
    #     queryset=Product.objects.all(),
    #     widget=RelatedFieldWidgetCanAdd(Product)
    # )

    class Meta:
        model = Order
        fields = ['product', 'manager', 'address', 'name',
                  'phone_number', 'volume', 'description',
                  'status', 'tonar', 'time_of_receipt', 'payment',
                  'longitude', 'latitude', 'coordinate'
                  ]

        exclude = ['manager', 'status', 'longitude', 'latitude', 'coordinate']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 4}),
            'product': MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
        }


class EditOrderForm(NewOrderForm):
    pass


class UpdateOrderForm(ModelForm):
    class Meta:
        model = Order

        fields = ['provider', 'cost', 'status', 'time_completed']
        widgets = {
            'time_completed': HiddenInput(),
            'status': HiddenInput(),
            'provider': MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
        }


class OrderSearchForm(SearchForm):
    pass


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'cols': 40, 'rows': 4}),
        }

