from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView
from notifications.signals import notify

from order_app.models import Order
from .forms import CommentForm
from .models import Comment


class EditComment(UpdateView):
    model = Comment
    form_class = CommentForm
    # template_name_suffix = '_edit_form'
    template_name = 'comment_app/update_comment.html'


def add_comment_to_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    author = User.objects.get(username=request.user)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = author
            comment.order = order
            comment.save()

            if 'manager' in author.groups.values_list('name', flat=True):
                recipient = User.objects.filter(groups__name='supplier')
            else:
                recipient = User.objects.get(pk=order.author_id)

            notify.send(sender=author,
                        recipient=recipient,
                        action_object=order,
                        verb='''Добавил(а) коментарий к заказу 
                                <a href="{}">№{}</a>'''.format(
                                    order.get_absolute_url(),
                                    order.pk
                                )
                        )

            # обновление заказа чтоб поднялся на самый верх
            order.save()

            return redirect('order:order_detail', pk=order.pk)
    else:
        form = CommentForm()
    return render(request, 'comment_app/add_comment_to_order.html', {'form': form})