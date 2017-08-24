from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование')

    class Meta:
        verbose_name = "Наименование"
        verbose_name_plural = "Наименования"
        ordering = ['name']

    def __str__(self):
        return self.name
