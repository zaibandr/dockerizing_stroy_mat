from haystack import indexes

from .models import Order


class OrderIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    product = indexes.IntegerField(model_attr='product_id')
    phone_number = indexes.CharField(model_attr='phone_number')
    description = indexes.CharField(model_attr='description')
    name = indexes.CharField(model_attr='name')

    created = indexes.DateTimeField(model_attr='created')
    suggestions = indexes.FacetCharField()

    # for spatial search
    location = indexes.LocationField()

    # for autocomplete.
    address = indexes.EdgeNgramField(model_attr='address')

    def prepare(self, obj):
        prepared_data = super(OrderIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def prepare_location(self, obj):
        return "%s,%s" % (obj.latitude, obj.longitude)

    def get_model(self):
        return Order

    def index_queryset(self, using=None):
        return self.get_model().objects.all()  # .order_by('time_created')
