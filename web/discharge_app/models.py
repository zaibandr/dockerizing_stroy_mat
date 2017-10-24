from django.db import models

from customer_app.models import Customer
from provider_app.models import Provider


class DischargeInput(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/', unique_for_date=True)
    date_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(unique_for_date=True)
    json = models.TextField(editable=False, verbose_name="json")

    def file_path(self):
        return self.file.path

    class Meta:
        verbose_name = "Выписка Банка"
        verbose_name_plural = "Выписки Банка"


class DischargeProvider(models.Model):
    provider = models.ForeignKey(Provider)
    action_choice = (
        (1, 'Пополнение'),
        (0, 'Снятие'),
    )

    action = models.IntegerField(choices=action_choice, verbose_name='Операция')
    value = models.FloatField(verbose_name='Сумма')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = "Выписка поставщика"
        verbose_name_plural = "Выписки поставщика"

    def save(self, *args, **kwargs):
        p = Provider.objects.get(pk=self.provider_id)
        if self.action:
            p.balance_add(int(self.value))
        else:
            p.balance_take_down(self.value)
        p.save()

        super(DischargeProvider, self).save(*args, **kwargs)


class DischargeCustomer(models.Model):
    customer = models.ForeignKey(Customer)
    action_choice = (
        (1, 'Пополнение'),
        (0, 'Снятие'),
    )

    action = models.IntegerField(choices=action_choice, verbose_name='Операция')
    value = models.FloatField(verbose_name='Сумма')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = "Выписка заказчика"
        verbose_name_plural = "Выписки заказчика"

    def save(self, *args, **kwargs):
        c = Customer.objects.get(pk=self.customer_id)
        if self.action:
            c.balance_add(int(self.value))
        else:
            c.balance_take_down(self.value)
        c.save()

        super(DischargeCustomer, self).save(*args, **kwargs)