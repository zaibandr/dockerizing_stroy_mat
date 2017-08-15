from django.db import models


class Zone(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    polygon = models.TextField(verbose_name='Полигон')

    class Meta:
        verbose_name = 'Зона'
        verbose_name_plural = 'Зоны'

    def __str__(self):
        return self.name
