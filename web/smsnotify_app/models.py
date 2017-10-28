from django.db import models

from order_app.models import Order
from provider_app.models import Provider


class SmsNotify(models.Model):
    order = models.ForeignKey(Order)
    provider = models.ForeignKey(Provider)
    sms_id = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    time_created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "СМС уведомление"
        verbose_name_plural = "СМС уведомления"