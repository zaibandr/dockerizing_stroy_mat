from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.views.generic.edit import UpdateView

from django.contrib.auth.models import User, Group
from order_app.models import Order
from provider_app.models import Product
from order_app.forms import NewOrderForm, EditOrderForm, MultiOrderForm, OrderFormSet
from django.forms import formset_factory

from geopy.geocoders import Yandex


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger('stroy_mat.order_app.manager')


def new_order_with_formset(request):
    if request.method == 'POST':
        action = request.POST.get('action', default=None)
        if action == "+":
            extra = int(float(request.POST['extra'])) + 1
            form = MultiOrderForm(request.POST)
            formset = formset_factory(OrderFormSet, extra=extra)
        else:
            extra = int(float(request.POST['extra']))
            form = MultiOrderForm(request.POST)
            formset = formset_factory(OrderFormSet, extra=extra)

            if form.is_valid():
                new_order = form.save(commit=False)
                for i in range(extra):
                    try:
                        order_dict = {
                            'address': new_order.address,
                            'description': new_order.description,
                            'name': new_order.name,
                            'payment': new_order.payment,
                            'phone_number': new_order.phone_number,
                            'time_of_receipt': new_order.time_of_receipt,
                            'tonar': new_order.tonar,
                            'product': Product.objects.get(pk=int(request.POST['form-{}-product'.format(i)])),
                            'volume': int(request.POST['form-{}-volume'.format(i)]),
                            'manager': User.objects.get(username=request.user),
                        }
                    except Exception as e:
                        log_title = 'функция new_order_with_formset \n'
                        log_msg = 'user {}:{}\t{}'.format(request.user, e, request.POST)

                        msg = log_title + log_msg
                        logger.error(msg)
                    else:
                        o = Order.objects.create(**order_dict)
                        o.save()

                last_oder = Order.objects.last()
                last_order_url = last_oder.get_absolute_url()

                return HttpResponseRedirect(last_order_url)
    else:
        form = MultiOrderForm()
        extra = 1
        formset = formset_factory(OrderFormSet, extra=extra)

    context = {
        'form': form,
        'formset': formset,
        'extra': extra
    }

    return render(request, "order_app/manager/order_formset.html", context=context)


def multi_order_create(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MultiOrderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            new_order = form.save(commit=False)

            new_order.manager = User.objects.get(username=request.user)

            new_order.save()

            last_oder = Order.objects.last()
            last_order_url = last_oder.get_absolute_url()

            return HttpResponseRedirect(last_order_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MultiOrderForm()

    return render(request, "order_app/manager/multi_order.html", {'form': form})


def new_order_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewOrderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            ###########################
            # set author field in form current user
            # https://stackoverflow.com/questions/18246326/in-django-how-do-i-set-user-field-in-form-to-the-currently-logged-in-user
            ###########################
            new_order = form.save(commit=False)

            new_order.manager = User.objects.get(username=request.user)

            # geo_locator = Yandex()
            # location = geo_locator.geocode(new_order.address, timeout=10)
            # new_order.longitude = location.longitude
            # new_order.latitude = location.latitude
            # new_order.coordinate = location.point

            new_order.save()

            last_oder = Order.objects.last()
            last_order_url = last_oder.get_absolute_url()

            return HttpResponseRedirect(last_order_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewOrderForm()

    return render(request, "order_app/manager/new_order.html", {'form': form})


class EditOrder(UpdateView):
    model = Order
    form_class = EditOrderForm
    # template_name_suffix = '_edit_form'
    template_name = 'order_app/manager/order_edit_form.html'
