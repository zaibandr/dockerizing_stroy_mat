from django.db import models
from django.urls import reverse

from core.models import OwnerModel
from order_app.models import Order


class Comment(OwnerModel, models.Model):
    order = models.ForeignKey(Order)
    text = models.TextField(max_length=300)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"

    def get_absolute_url(self):
        return reverse('order:order_detail', kwargs={'pk': self.order_id})

    def __str__(self):
        return '{} \t({})'.format(self.text, self.author.username)
