from .models import DischargeEntity, DischargeProvider, DischargeCustomer
from .tables import DischargeEntityTable, DischargeProviderTable, DischargeCustomerTable


class TransactionsMixin:
    def get_context_data(self, **kwargs):
        context = super(TransactionsMixin, self).get_context_data(**kwargs)

        ds_entity = DischargeEntity.objects.filter(entity__inn=self.object.inn)

        context['discharge_entity_table'] = DischargeEntityTable(
            ds_entity
        )
        context['ds_entity_debet'] = sum(ds_entity.values_list('debet', flat=True))
        context['ds_entity_credit'] = sum(ds_entity.values_list('credit', flat=True))

        ds_provider = DischargeProvider.objects.filter(provider__inn=self.object.inn)
        context['discharge_provider_table'] = DischargeProviderTable(
            ds_provider
        )
        context['ds_provider_values_sum'] = sum(ds_provider.values_list('value', flat=True))

        ds_customer = DischargeCustomer.objects.filter(customer__inn=self.object.inn)
        context['discharge_customer_table'] = DischargeCustomerTable(
            ds_customer
        )
        context['ds_customer_values_sum'] = sum(ds_customer.values_list('value', flat=True))

        return context
