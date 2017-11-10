from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django_tables2 import RequestConfig

from .forms import NewShipmentForm, EditShipmentForm
from .models import Shipment
from .tables import ShipmentTable


@login_required()
def shipments(request):
    if request.user.is_staff:
        all_shipment_sqs = Shipment.objects.all()
    else:
        all_shipment_sqs = Shipment.objects.filter(author=request.user)

    all_shipment = ShipmentTable(all_shipment_sqs)

    RequestConfig(request).configure(all_shipment)
    all_shipment.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'shipments': all_shipment,
    }

    return render(request, 'shipment_app/shipment_list.html', context)


class ShipmentDetailView(DetailView):

    model = Shipment

    # @cached_as(Provider, timeout=60*10)
    def get_context_data(self, **kwargs):
        context = super(ShipmentDetailView, self).get_context_data(**kwargs)

        return context


class ShipmentAdd(CreateView):
    model = Shipment
    form_class = NewShipmentForm
    template_name = 'shipment_app/new_shipment.html'


def new_shipment_form(request):

    if request.method == 'POST':

        form = NewShipmentForm(request.POST)

        if form.is_valid():
            ###########################
            # set author field in form current user
            # https://stackoverflow.com/questions/18246326/in-django-how-do-i-set-user-field-in-form-to-the-currently-logged-in-user
            ###########################
            new_shipment = form.save(commit=False)

            new_shipment.author= User.objects.get(username=request.user)

            new_shipment.save()

            # last_shipment_url = Shipment.objects.last().get_absolute_url()
            return redirect('shipment:shipments_list')

    else:
        form = NewShipmentForm()

    return render(request, "shipment_app/new_shipment.html", {'form': form})


class EditShipment(UpdateView):
    model = Shipment
    form_class = EditShipmentForm

    template_name = 'shipments/shipment_edit_form.html'
