import json

from django.http import HttpResponse
from django.shortcuts import render
from django_tables2 import RequestConfig
# from haystack.inputs import AutoQuery, Clean
from haystack.query import SearchQuerySet

from order_app.forms import OrderSearchForm
from order_app.models import Order
from order_app.tables import OrdersTable


def sqs_to_qs(search_qs):
    for item in search_qs:
        yield item.object


def autocomplete_order_id(request):
    sqs = SearchQuerySet().autocomplete(text=request.GET.get('q', '')).highlight()[:10]
    suggestions = [result.pk for result in sqs]

    the_data = json.dumps([{'order': i} for i in suggestions])
    return HttpResponse(the_data, content_type='application/json')


def autocomplete_order_address(request):
    sqs = SearchQuerySet().autocomplete(text=request.GET.get('q', ''))[:10]
    suggestions = [result.address for result in sqs]

    clear_suggestions = []
    d = {}
    for s in suggestions:
        if s not in d:
            clear_suggestions.append(s)
            d[s] = True

    the_data = json.dumps([{'address': i} for i in clear_suggestions])
    return HttpResponse(the_data, content_type='application/json')


def order_search_form(request):

    form = OrderSearchForm(request.GET)
    search_sqs = form.search()

    # Elastic return list to django SQS
    # https://stackoverflow.com/questions/13642617/django-haystack-searchqueryset-to-queryset

    order_pk = [order.pk for order in [i.object.pk for i in search_sqs]]
    orders = Order.objects.filter(pk__in=order_pk).select_related('product')

    # SQS to table (django-table2)
    orders = OrdersTable(orders)

    RequestConfig(request).configure(orders)
    # orders.paginate(page=request.GET.get('page', 1), per_page=20)

    context = {
        'orders': orders,
        'query': request.GET.get('q', ''),
    }
    # print(context)

    return render(request, 'order_app/order_search.html', context)
