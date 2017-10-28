from django.db import models
from djgeojson.fields import PolygonField, PointField

from core.models import DescriptionModel


class Product(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование', db_index=True)

    class Meta:
        verbose_name = "Наименование"
        verbose_name_plural = "Наименования"
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductGeo(DescriptionModel, models.Model):
    products = models.ManyToManyField(Product, verbose_name='Продукция', db_index=True)
    delivery_region = PolygonField(default='[]',)
    pick_point = PointField()

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'

    def __str__(self):
        return self.description

