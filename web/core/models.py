from django.contrib.auth.models import User
from django.db import models

from django.contrib.postgres.fields import JSONField


class AttributesModel(models.Model):
    attributes = JSONField(verbose_name='Атрибуты', default={})

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_index=True)
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', db_index=True)

    class Meta:
        abstract = True


class OwnerModel(models.Model):
    author = models.ForeignKey(User)

    class Meta:
        abstract = True


class DescriptionModel(models.Model):
    description = models.TextField(max_length=600, blank=True, verbose_name='Описание')

    class Meta:
        abstract = True


class BalanceModel(models.Model):
    balance = models.FloatField(editable=False, default=0, verbose_name='Баланс')

    saldo_debet = models.FloatField(default=0, verbose_name='Сальдо дебет')
    saldo_credit = models.FloatField(default=0, verbose_name='Сальдо кредит')
    saldo_date = models.DateField(null=True, default=None, blank=True, verbose_name='Салбдо дата')

    class Meta:
        abstract = True

    def update_balance(self):
        from discharge_app.models import DischargeEntity, DischargeProvider, DischargeCustomer

        balance = self.saldo_credit - self.saldo_debet
        for discharge in DischargeCustomer.objects.filter(customer__inn=self.inn):
            if self.__class__.__name__ == 'Customer':
                balance -= discharge.value
            else:
                balance += discharge.value

        for discharge in DischargeProvider.objects.filter(provider__inn=self.inn):
            if self.__class__.__name__ == 'Provider':
                balance -= discharge.value
            else:
                balance += discharge.value

        # транзакции с выписки банка
        for de in DischargeEntity.objects.filter(entity__inn=self.inn):
            if self.__class__.__name__ == 'Provider':
                balance += de.debet - de.credit
            elif self.__class__.__name__ == 'Customer':
                balance += de.credit - de.debet

        self.balance = balance
        self.save()


class MailModel(models.Model):
    mail_1 = models.EmailField(blank=True, null=True, verbose_name='mail_1')
    mail_2 = models.EmailField(blank=True, null=True, verbose_name='mail_2')

    class Meta:
        abstract = True


class PhoneNumberModel(models.Model):
    phone_number = models.CharField(max_length=12, null=True, blank=True, verbose_name='Номер телефона')
    sms_phone_number = models.CharField(max_length=12, null=True, blank=True, verbose_name='Номер для отправки СМС')

    class Meta:
        abstract = True


class ContactNameModel(models.Model):
    contact_name = models.TextField(max_length=200, blank=True, verbose_name='Контакты')

    class Meta:
        abstract = True


class DeliveryModel(models.Model):
    address = models.CharField(max_length=200, null=True, verbose_name='Адрес', )
    longitude = models.FloatField(blank=True, null=True, verbose_name='Долгота')
    latitude = models.FloatField(blank=True, null=True, verbose_name='Широта')
    coordinate = models.CharField(blank=True, null=True, max_length=100, verbose_name='Координаты')

    class Meta:
        abstract = True

    def _address_prepare(self):
        from geopy.geocoders import Yandex

        geo_locator = Yandex()
        location = geo_locator.geocode(self.address, timeout=10)
        if location is None:
            location = geo_locator.geocode('г Москва', timeout=10)
            self.address = "Невозможно найти адрес! Убедитесь что адрес верный и повторите ввод."

        self.longitude = location.longitude
        self.latitude = location.latitude
