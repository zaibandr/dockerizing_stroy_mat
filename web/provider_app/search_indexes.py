from haystack import indexes

from .models import Provider


class ProviderIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    name = indexes.CharField(model_attr='name')
    contact_name = indexes.CharField(model_attr='contact_name')
    # phone_number = indexes.CharField(model_attr='phone_number')

    # products = indexes.MultiValueField()
    #
    # def prepare_products(self, obj):
    #     return [product.name for product in obj.products.all()]

    # def prepare(self, obj):
    #     prepared_data = super(ProviderIndex, self).prepare(obj)
    #     prepared_data['suggestions'] = prepared_data['text']
    #     return prepared_data

    def get_model(self):
        return Provider

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
