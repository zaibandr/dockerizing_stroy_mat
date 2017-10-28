import datetime

from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from notifications.models import Notification
from notifications.signals import notify

from order_app.forms import UpdateOrderForm
from order_app.models import Order


class OrderUpdate(UpdateView):
    model = Order
    form_class = UpdateOrderForm

    # template_name_suffix = '_update_form'
    template_name = 'order_app/supplier/order_update_form.html'

    def form_valid(self, form):
        # send notify
        notify.send(sender=User.objects.get(username=self.request.user),
                    recipient=User.objects.get(pk=self.object.manager_id),
                    action_object=self.object,
                    verb='''Обновил(а) заказ
                            <a href="{}">№{}</a>'''.format(
                            self.object.get_absolute_url(),
                            self.object.pk
                        )
                    )

        return super(OrderUpdate, self).form_valid(form)

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        print(request.POST)
        print(request.POST['time_completed'])
        if request.POST['provider'] == '0' or request.POST['cost'] == '0':
            request.POST['status'] = 'CRTD'
            request.POST['time_completed'] = None
        else:
            # Заказ обработан
            # Пометить прочитанными уведомления данного заказа для всех снабженцов
            group_name = User.objects.get(username=request.user).groups.values_list('name', flat=True)
            user_pks = User.objects.filter(groups__name=group_name).values_list('pk', flat=True)
            for n in Notification.objects.filter(
                                    recipient_id__in=user_pks,
                                    action_object_object_id=self.get_object().pk):
                n.mark_as_read()

            request.POST['time_completed'] = datetime.datetime.now()

        return super(OrderUpdate, self).post(request, **kwargs)
