# import the logging library
import logging

from django.contrib.auth.models import User
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import UpdateView

from order_app.forms import NewOrderForm, EditOrderForm, MultiOrderForm, OrderFormSet
from order_app.models import Order
from product_app.models import Product

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
                            'author': User.objects.get(username=request.user),
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


class EditOrder(UpdateView):
    model = Order
    form_class = EditOrderForm
    # template_name_suffix = '_edit_form'
    template_name = 'order_app/manager/order_edit_form.html'
