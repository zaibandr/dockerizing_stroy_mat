from django.forms import ModelForm, Textarea, ModelChoiceField, IntegerField, HiddenInput, Form

from haystack.query import SQ, AutoQuery, SearchQuerySet
from haystack.forms import SearchForm

from core.forms import MySelect
from product_app.models import Product
from .models import Order


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
    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        q = self.cleaned_data['q']
        sqs = self.searchqueryset.filter(
            SQ(description=AutoQuery(q))
            #SQ(text=AutoQuery(q)) | SQ(description=AutoQuery(q)) | SQ(address=AutoQuery(q))
        )

        if self.load_all:
            sqs = sqs.load_all()

        return sqs.highlight()