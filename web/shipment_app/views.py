from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django_tables2 import RequestConfig, SingleTableView

from .forms import NewShipmentForm, UpdateShipmentManagerForm, UpdateShipmentSupplierForm, UpdateShipmentBookerForm
from .models import Shipment
from .tables import ShipmentTable
from .tables import ManagerShipmentTable, SupplierShipmentTable, BookerShipmentTable


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


class ShipmentList(LoginRequiredMixin, SingleTableView):
    model = Shipment
    template_name = 'shipment_app/shipment_list.html'

    table_class = ''

    table_pagination = {
        'per_page': 10
    }

    def get_queryset(self):
        group_name = User.objects.get(username=self.request.user).groups.values_list('name', flat=True)
        if 'manager' in group_name:
            self.queryset = Shipment.objects.filter(author=self.request.user)
        else:
            self.queryset = Shipment.objects.all()

        return self.queryset

    def get_table_class(self):
        group_name = User.objects.get(username=self.request.user).groups.values_list('name', flat=True)
        if 'manager' in group_name:
            self.table_class = ManagerShipmentTable
        elif 'supplier' in group_name:
            self.table_class = SupplierShipmentTable
        else:
            self.table_class = BookerShipmentTable
        return self.table_class


class ShipmentDetailView(LoginRequiredMixin, DetailView):

    model = Shipment

    # @cached_as(Provider, timeout=60*10)
    def get_context_data(self, **kwargs):
        context = super(ShipmentDetailView, self).get_context_data(**kwargs)

        return context


class ShipmentAdd(LoginRequiredMixin, CreateView):
    model = Shipment
    form_class = NewShipmentForm
    template_name = 'shipment_app/new_shipment.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return redirect('shipment:shipments_list')


def new_shipment_form(request):

    if request.method == 'POST':

        form = NewShipmentForm(request.POST)

        if form.is_valid():
            ###########################
            # set author field in form current user
            # https://stackoverflow.com/questions/18246326/in-django-how-do-i-set-user-field-in-form-to-the-currently-logged-in-user
            ###########################
            new_shipment = form.save(commit=False)

            new_shipment.author = User.objects.get(username=request.user)

            new_shipment.save()

            # last_shipment_url = Shipment.objects.last().get_absolute_url()
            return redirect('shipment:shipments_list')

    else:
        form = NewShipmentForm()

    return render(request, "shipment_app/new_shipment.html", {'form': form})


class EditShipment(LoginRequiredMixin, UpdateView):
    model = Shipment
    form_class = ''

    template_name = 'shipment_app/shipment_edit_form.html'

    def get_form_class(self):
        #super(EditShipment, self).get_form_class()
        group_name = User.objects.get(username=self.request.user).groups.values_list('name', flat=True)
        if 'manager' in group_name:
            self.form_class = UpdateShipmentManagerForm
        elif 'supplier' in group_name:
            self.form_class = UpdateShipmentSupplierForm
        else:
            self.form_class = UpdateShipmentBookerForm
        return self.form_class

    def get_context_data(self, **kwargs):
        context = super(EditShipment, self).get_context_data(**kwargs)
        context['data'] = self.object.get_data_json()

        return context
