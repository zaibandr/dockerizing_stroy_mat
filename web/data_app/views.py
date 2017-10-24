from django.shortcuts import render, get_object_or_404, redirect

from order_app.models import Order
import datetime

from cacheops import cached_as, cached_view_as


@cached_as(Order, timeout=60*60*4)
def provider_orders(request):

    product_d = {}

    for order in Order.objects.filter(status='CMPLTD'):
        product_d[order.product.name] = 1

    products = sorted(product_d.keys())

    series = {}
    for order in Order.objects.filter(status='CMPLTD'):

        d = {
            'name': order.provider.name,
            'data': [order.product.name]
        }
        if order.provider.name not in series:
            series[order.provider.name] = d
        else:
            series[order.provider.name]['data'] += d['data']

    series = list(series.values())
    for s in series:
        data = []
        for p in products:
            data.append(s['data'].count(p))
        s['data'] = data

    context = {
        'products': products,
        'series': sorted(series, key=lambda x: sum(x['data']), reverse=True)
    }

    return render(request, 'data_app/provider_orders.html', context)


@cached_as(Order, timeout=60*60*4)
def orders_per_day(request):
    days = {}
    for order in Order.objects.all():
        date = order.time_created.date().strftime('%d.%m.%Y')
        if date not in days:
            days[date] = 1
        else:
            days[date] += 1

    context = {
        'days': days,
        'categories': [k for k, v in sorted(days.items(), key=lambda x: datetime.datetime.strptime(x[0], '%d.%m.%Y'))],
        'data': [v for k, v in sorted(days.items(), key=lambda x: datetime.datetime.strptime(x[0], '%d.%m.%Y'))]
    }

    return render(request, 'data_app/orders_per_day.html', context)


@cached_as(Order, timeout=60*60*4)
def overage_complete_time(request):
    days = {}
    for order in Order.objects.filter(status='CMPLTD'):
        date = order.time_completed.date().strftime('%d.%m.%Y')
        if date == order.time_created.date().strftime('%d.%m.%Y'):
            if date not in days:
                days[date] = [order.time_completed - order.time_created]
            else:
                days[date] += [order.time_completed - order.time_created]

    days_overage = {}

    for k, v in days.items():
        days_overage[k] = sum([i.total_seconds()/60 for i in v])/len(v)

    days_median = {}

    def median(array):
        a = sorted(array)
        if len(a) % 2 == 0:
            return (a[int(len(a)/2)] + a[int(len(a)/2)-1])/2
        else:
            return a[int(len(a)/2)]

    for k, v in days.items():
        days_median[k] = median([i.total_seconds()/60 for i in v])

    context = {
        'days': [k for k, v in sorted(days.items(), key=lambda x: datetime.datetime.strptime(x[0], '%d.%m.%Y'))],
        'days_overage': [v for k, v in sorted(days_overage.items(), key=lambda x: datetime.datetime.strptime(x[0], '%d.%m.%Y'))],
        'days_median': [v for k, v in sorted(days_median.items(), key=lambda x: datetime.datetime.strptime(x[0], '%d.%m.%Y'))]
    }

    return render(request, 'data_app/overage_complete_time.html', context)


@cached_as(Order, timeout=60*60*4)
def all_order_on_map(request):
    all_order = Order.objects.all()

    context = {
        'all_order': all_order
    }

    return render(request, 'data_app/all_order_on_map.html', context)


def get_real_ip(request):
    return render(request, 'qq')


@cached_as(Order, timeout=60*60*4)
def order_triangle(request):
    import numpy as np
    from scipy.spatial import Delaunay
    from shapely.geometry import Polygon

    orders = Order.objects.filter(product_id=1, status='CMPLTD', cost__gt=0, cost__lt=650)
    points = np.array([[o.latitude, o.longitude] for o in orders])
    tri = Delaunay(points)

    areas = []
    polys = []
    for index, tr in enumerate(points[tri.simplices]):
        poly = tr.tolist() + [tr.tolist()[0]]
        areas.append(Polygon(poly).area)
        triangle_cost = 0
        for p in tr.tolist():
            order = Order.objects.filter(latitude=p[0], longitude=p[1], product_id=1, cost__gt=0, cost__lt=650).last()
            triangle_cost += order.cost
        triangle_cost /= 3
        name = 'poly_{}'.format(str(index))
        polys.append((poly, name, triangle_cost))

    areas = sorted(areas, reverse=True)
    a = [areas[i] for i in range(0, len(areas), len(areas)//20)]
    areas_percent = a[(len(a)-20)//2:-(len(a)-20)//2]
    overage_cost = sum([cost for _, _, cost in polys])/len(polys)

    triangles = []
    for poly, name, triangle_cost in polys:
        poly_a = Polygon(poly).area
        for i, a, in enumerate(areas_percent, start=1):
            if poly_a >= a:
                percent = i*5/100
                popup = '{}*{}+{}*{}={}'.format(format(triangle_cost, '.2f'),
                                                format(1-(1-percent), '.2f'),
                                                format(overage_cost, '.2f'),
                                                format(1-percent, '.2f'),
                                                format(triangle_cost*(1-(1-percent))+overage_cost*(1-percent), '.2f'),
                                                )
                triangles.append((poly, name, popup))
                break

    context = {
        'triangles': triangles,
        'orders': orders,
        'areas': areas
    }
    return render(request, 'data_app/order_triangle.html', context)



