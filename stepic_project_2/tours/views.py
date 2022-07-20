import random

from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

import tours.data as dt


# Create your views here.
def main_view(request):
    tours_sample = dict(random.sample(dt.tours.items(), 6))
    context = dict()
    correct_data = {}
    for id, data in tours_sample.items():
        data['card_url'] = data['picture'].replace('&w=800&q=60', '&w=300&h=200')
        data['price_view'] = '{:,}'.format(data['price']).replace(',', ' ')
        correct_data[id] = data
    context['h1'] = "Всякие туры"
    context['p1'] = dt.subtitle
    context['p2'] = dt.description
    context['data'] = correct_data
    return render(request, "index.html", context=context)


def departure_view(request, departure):
    filter_tours = dict([x for x in dt.tours.items() if x[1]['departure'] == departure])
    context = dict()
    context['dep_name'] = dt.departures.get(departure).split(' ')[-1]
    context['cnt_tours'] = len(filter_tours)
    context['min_price'] = '{:,}'.format(min([filter_tours[x]['price'] for x in filter_tours])).replace(',', ' ')
    context['max_price'] = '{:,}'.format(max([filter_tours[x]['price'] for x in filter_tours])).replace(',', ' ')
    context['min_date'] = min([filter_tours[x]['nights'] for x in filter_tours])
    context['max_date'] = max([filter_tours[x]['nights'] for x in filter_tours])
    correct_data = {}
    for id, data in filter_tours.items():
        data['card_url'] = data['picture'].replace('&w=800&q=60', '&w=300&h=200')
        data['price_view'] = '{:,}'.format(data['price']).replace(',', ' ')
        correct_data[id] = data
    context['data'] = correct_data
    return render(request, "departure.html", context=context)


def tour_view(request, id):
    tour = dt.tours.get(id, False)
    st = [x for x in range(int(tour['stars']))]
    if tour is False:
        return HttpResponseNotFound("Нет такого тура! Выбери другой.")
    context = tour
    context['rangeSt'] = st
    context['price_view'] = '{:,}'.format(context['price']).replace(',', ' ')
    dep_list = {
        "nsk": "Из Новосибирска",
        "ekb": "Из Екатеринбурга",
        "msk": "Из Москвы",
        "spb": "Из Петербурга",
        "kazan": "Из Казани"
    }
    context['dep_name'] = dep_list.get(context.get('departure'))
    return render(request, "tour.html", context=context)


def custom_handler404(request, exception):
    # Call when Http404 raised
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')
