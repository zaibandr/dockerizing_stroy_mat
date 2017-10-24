import django_tables2 as tables
from django.utils.html import format_html, mark_safe
from .models import Order
from notifications.models import Notification


class ProductColumn(tables.Column):
    def render(self, value, record):
        return format_html('<a href="/order/detail/{}/"><p class="text-left">{}</p></a>', record.pk, value)


class TimeColumn(tables.Column):
    def render(self, record, value):
        if record.time_completed is not None:
            return int((record.time_completed - record.time_created).total_seconds()/60)
        return '-'


class OrdersTable(tables.Table):
    status = tables.Column()
    product = ProductColumn(verbose_name='Product')
    time = TimeColumn(empty_values=())
    unred_order_pk = []

    def before_render(self, request):
        self.unred_order_pk = list(Notification.objects.filter(
            recipient=request.user,
            unread=True).values_list('action_object_object_id', flat=True))

    def render_status(self, record, value):
        if str(record.pk) in self.unred_order_pk:
            status = 'Непрочитан'
            return format_html('<span class="label label-info">{}</span>'.format(status))
        return value

    class Meta:
        model = Order
        order_by = '-time_updated'

        # add class="paleblue" to <table> tag
        fields = ('id', 'product', 'volume', 'status', 'phone_number',
                  'address', 'manager', 'time_created', 'time_updated')

        row_attrs = {
            'class': lambda
                record: 'info' if record.status == 'UNREAD' else 'success' if record.status == 'CMPLTD' else 'danger'
        }


class SimilarOrderTable(tables.Table):
    product = ProductColumn(verbose_name='Product')
    provider = tables.Column(verbose_name='Поставщик')

    def render_provider(self, record, value):
        return format_html('<a href="/provider/detail/{}/"><p class="text-left">{}</p></a>', record.provider_id, value)

    class Meta:
        model = Order
        fields = ('pk', 'product', 'cost', 'volume', 'address', 'provider_id', 'provider')

