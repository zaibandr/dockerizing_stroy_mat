import django_filters
from django.forms import Select

from product_app.models import Product
from .models import Provider


class MySelect(Select):
    def render_option(self, selected_choices, option_value, option_label):
        # look at the original for something to start with
        return '<option value="{}" data-tokens="{}">{}</option>'.format(option_value, str(option_label).lower(), option_label)


class ProviderFilter(django_filters.FilterSet):
    products = django_filters.ChoiceFilter(choices=Product.objects.all().values_list('pk', 'name'),
                                           widget=MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
                                           )

    class Meta:
        model = Provider
        fields = []
