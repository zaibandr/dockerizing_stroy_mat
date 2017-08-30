from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.views.generic.edit import UpdateView

from django.contrib.auth.models import User, Group
from has_app.models import Order, Shipment, Comment
from has_app.forms import NewOrderForm, EditOrderForm
from has_app.forms import NewShipmentForm, EditShipmentForm

from geopy.geocoders import Yandex

from notifications.signals import notify


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

            geo_locator = Yandex()
            location = geo_locator.geocode(new_order.address, timeout=10)
            new_order.longitude = location.longitude
            new_order.latitude = location.latitude
            new_order.coordinate = location.point

            new_order.save()

            last_oder = Order.objects.last()
            last_order_url = last_oder.get_absolute_url()

            # send notify
            notify.send(sender=User.objects.get(username=request.user),
                        recipient=User.objects.filter(groups=2),
                        verb='''Создал(а) новый заказ 
                                <a href="{}">№{}</a>'''.format(
                                    last_oder.get_absolute_url(),
                                    last_oder.pk
                                )
                        )

            return HttpResponseRedirect(last_order_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewOrderForm()

    return render(request, "has_app/manager/new_order.html", {'form': form})


class EditOrder(UpdateView):
    model = Order
    form_class = EditOrderForm
    # template_name_suffix = '_edit_form'
    template_name = 'has_app/manager/order_edit_form.html'

    def form_valid(self, form):
        # send notify
        notify.send(sender=User.objects.get(username=self.request.user),
                    recipient=User.objects.filter(groups=2),
                    verb='''Изменил(а) заказ 
                            <a href="{}">№{}</a>'''.format(
                            self.object.get_absolute_url(),
                            self.object.pk
                        )
                    )

        return super(EditOrder, self).form_valid(form)


def new_shipment_form(request):

    if request.method == 'POST':

        form = NewShipmentForm(request.POST)

        if form.is_valid():
            ###########################
            # set author field in form current user
            # https://stackoverflow.com/questions/18246326/in-django-how-do-i-set-user-field-in-form-to-the-currently-logged-in-user
            ###########################
            new_shipment = form.save(commit=False)

            new_shipment.manager = User.objects.get(username=request.user)

            new_shipment.profit = (new_shipment.cost_out - new_shipment.cost_in) * new_shipment.volume
            new_shipment.price = new_shipment.cost_out * new_shipment.volume

            new_shipment.save()

            # last_shipment_url = Shipment.objects.last().get_absolute_url()
            return HttpResponseRedirect('/shipments/')

    else:
        form = NewShipmentForm()

    return render(request, "has_app/manager/new_shipment.html", {'form': form})


class EditShipment(UpdateView):
    model = Shipment
    form_class = EditShipmentForm

    template_name = 'has_app/manager/shipment_edit_form.html'
