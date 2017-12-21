import tablib

from django.core.mail import send_mail, EmailMessage

from order_app.models import Order


def email_order_excel(to_mail='panagoa@ya.ru'):
    import datetime
    data = tablib.Dataset(headers=['№', 'наименование', 'адрес'])

    for order in Order.objects.all().values_list('pk', 'product__name', 'address'):
        data.append(order)

    file_name = 'Все заказы на {}.xls'.format(datetime.datetime.now().date().strftime('%d.%m.%Y'))
    file = data.export('xls')
    mail = EmailMessage('foo', 'bar', 'zaibandr@ya.ru', [to_mail])

    mail.attach(filename=file_name, content=file, mimetype='application/excel')

    return mail.send()
