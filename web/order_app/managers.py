from django.db import models


class NearSimilarOrderManager(models.Manager):
    use_for_related_fields = True

    def near_similar_order(self, point_longitude: float, point_latitude: float, product_id:int, km: int=10):
        from haystack.query import SearchQuerySet
        from haystack.utils.geo import Point, D
        point = Point(point_longitude, point_latitude)

        sqs = SearchQuerySet().filter(product=product_id).dwithin(
            'location',
            point,
            D(km=km)
        ).distance('location', point).order_by('distance')
        return sqs