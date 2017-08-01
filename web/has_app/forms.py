from django.forms import ModelForm, Textarea, HiddenInput, Select
from .models import Order, Product
from haystack.forms import SearchForm


# https://stackoverflow.com/questions/28068168/django-adding-an-add-new-button-for-a-foreignkey-in-a-modelform
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets, ModelChoiceField
from django.conf import settings


class RelatedFieldWidgetCanAdd(widgets.Select):

    def __init__(self, related_model, related_url=None, *args, **kw):

        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = 'admin:%s_%s_add' % info

        # Be careful that here "reverse" is not allowed
        self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        print(self.related_url)
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
        output.append('<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
            (self.related_url, name))
        output.append('<img src="%sadmin/img/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (settings.STATIC_URL, 'Add Another'))
        return mark_safe(''.join(output))


class MySelect(Select):
    def render_option(self, selected_choices, option_value, option_label):
        # look at the original for something to start with
        return '<option value="{}" data-tokens="{}">{}</option>'.format(option_value, str(option_label).lower(), option_label)


class NewOrderForm(ModelForm):
    # product = ModelChoiceField(
    #     required=False,
    #     queryset=Product.objects.all(),
    #     widget=RelatedFieldWidgetCanAdd(Product)
    # )

    class Meta:
        model = Order
        fields = ['product', 'manager', 'address', 'name', 'phone_number', 'volume', 'description', 'status', 'tonar', 'time_of_receipt', 'payment']
        exclude = ['manager', 'status']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 4}),
            'product': MySelect(attrs={'class': 'selectpicker', 'data-live-search': 'true'})

        }


class EditOrderForm(NewOrderForm):
    pass


class UpdateOrderForm(ModelForm):
    class Meta:
        model = Order

        fields = ['cost', 'status', 'time_completed']
        widgets = {'time_completed': HiddenInput()}


class OrderSearchForm(SearchForm):
    pass
