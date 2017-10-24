from haystack import indexes
from .models import Order


class OrderIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    phone_number = indexes.CharField(model_attr='phone_number')
    description = indexes.CharField(model_attr='description')
    name = indexes.CharField(model_attr='name')

    # We add this for autocomplete.
    address = indexes.CharField(model_attr='address')
    content_auto = indexes.EdgeNgramField(model_attr='address')
    time_created = indexes.DateTimeField(model_attr='time_created')

    suggestions = indexes.FacetCharField()

    def prepare(self, obj):
        prepared_data = super(OrderIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def get_model(self):
        return Order

    def index_queryset(self, using=None):
        return self.get_model().objects.all()  # .order_by('time_created')
