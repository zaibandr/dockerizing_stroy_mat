from django.urls import reverse
from django.db import models
import datetime

from core.models import ContactNameModel, DescriptionModel, PhoneNumberModel, BalanceModel


class Customer(ContactNameModel, DescriptionModel, PhoneNumberModel, BalanceModel, models.Model):

    name = models.CharField(max_length=100, verbose_name='Имя', db_index=True)
    individual_person = models.BooleanField(default=False, verbose_name='Физическое лицо')

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('customer_detail', kwargs={'pk': self.pk})


class CreditPayment(models.Model):
    customer = models.ForeignKey(Customer)
    amount = models.IntegerField(verbose_name='Сумма')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата Создания')
    paid_date = models.DateTimeField(editable=False, blank=True, null=True, verbose_name='Дата оплаты')
    balance_add = models.BooleanField(editable=False, default=False)
    balance_take_down = models.BooleanField(editable=False, default=False)

    class Meta:
        verbose_name = 'Доверительный платеж'
        verbose_name_plural = 'Доверительные платежи'

    def save(self, *args, **kwargs):
        if not self.balance_add:
            c = Customer.objects.get(pk=self.customer.pk)
            c.balance_add(self.amount)
            c.save()
            self.balance_add = True

        if self.paid:
            c = Customer.objects.get(pk=self.customer.pk)
            c.balance_take_down(self.amount)
            c.save()
            self.balance_take_down = True
            self.paid_date = datetime.datetime.now()

        super(CreditPayment, self).save(*args, **kwargs)