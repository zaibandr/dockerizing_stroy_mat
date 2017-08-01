import json
from django.shortcuts import render

from django.http import HttpResponse
from .models import Order

# from haystack.inputs import AutoQuery, Clean
from haystack.query import SearchQuerySet

from django_tables2 import RequestConfig
from .tables import OrdersTable
from .forms import OrderSearchForm


def sqs_to_qs(search_qs):
    for item in search_qs:
        yield item.object


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(text=request.GET.get('q', ''))[:10]
    suggestions = [result.content_auto for result in sqs]

    suggestions = [{'text': i} for i in suggestions]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps(suggestions)
    return HttpResponse(the_data, content_type='application/json')


def order_search_form(request):

    form = OrderSearchForm(request.GET)
    order_sqs = form.search()

    # Elastic return list to django SQS
    # https://stackoverflow.com/questions/13642617/django-haystack-searchqueryset-to-queryset
    orders = sqs_to_qs(order_sqs)
    order_pk = [order.pk for order in orders]
    orders = Order.objects.filter(pk__in=order_pk)

    # SQS to table (django-table2)
    orders = OrdersTable(orders)

    RequestConfig(request).configure(orders)
    # orders.paginate(page=request.GET.get('page', 1), per_page=20)

    context = {
        'orders': orders,
        'query': request.GET.get('q', ''),
    }
    # print(context)

    return render(request, 'has_app/order_search.html', context)
