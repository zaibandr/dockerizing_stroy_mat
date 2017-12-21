from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import django.core.exceptions as dj_exceptions

from shipment_app.models import Shipment
from discharge_app.models import DischargeProvider, DischargeCustomer, DischargeEntity

from provider_app.models import Provider
from customer_app.models import Customer


@receiver(post_save, sender=Shipment)
def create_discharge(sender, instance, **kwargs):
    import datetime

    main_data = {
        'action': DischargeProvider.ACTION_BALANCE_DOWN,
        'shipment_id': instance,
        'action_date': datetime.datetime.now().date().strftime('%d.%m.%Y'),
    }

    provider_data = {
        'provider_id': instance.provider_id,
        'value': instance.volume_m * instance.cost_in,
    }

    customer_data = {
        'customer_id': instance.customer_id,
        'value': instance.volume_m * instance.cost_out + instance.price_delivery,
    }

    try:
        dp = DischargeProvider.objects.get(shipment_id=instance)
        for key, value in provider_data.items():
            setattr(dp, key, value)
        dp.save()

        dc = DischargeCustomer.objects.get(shipment_id=instance)
        for key, value in customer_data.items():
            setattr(dc, key, value)
        dc.save()
    except dj_exceptions.ObjectDoesNotExist:
        dp_create_data = main_data.copy()
        dp_create_data.update(provider_data)

        DischargeProvider.objects.create(**dp_create_data)

        dc_create_data = main_data.copy()
        dc_create_data.update(customer_data)

        DischargeCustomer.objects.create(**dc_create_data)


@receiver(post_delete, sender=DischargeProvider)
@receiver(post_save, sender=DischargeProvider)
def update_provider_balance(sender, instance, **kwargs):
    p = Provider.objects.get(pk=instance.provider_id)
    p.update_balance()


@receiver(post_delete, sender=DischargeCustomer)
@receiver(post_save, sender=DischargeCustomer)
def update_customer_balance(sender, instance, **kwargs):
    c = Customer.objects.get(pk=instance.customer_id)
    c.update_balance()


@receiver(post_save, sender=DischargeEntity)
@receiver(post_delete, sender=DischargeEntity)
def update_balance(sender, instance, **kwargs):

    try:
        p = Provider.objects.get(inn=instance.entity.inn)
        p.update_balance()
    except dj_exceptions.ObjectDoesNotExist:
        pass

    try:
        c = Customer.objects.get(inn=instance.entity.inn)
        c.update_balance()
    except dj_exceptions.ObjectDoesNotExist:
        pass
