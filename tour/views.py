import random

from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render

import tour.data as dt


# Create your views here.
def main_view(request):
    count_tours_main = 6
    tours_sample = dict(random.sample(dt.tours.items(), count_tours_main))
    context = dict()
    correct_data = {}
    for tour_id, data in tours_sample.items():
        data['card_url'] = data['picture'].replace('&w=800&q=60', '&w=300&h=200')
        # data['price_view'] = '{:,}'.format(data['price']).replace(',', ' ')
        correct_data[tour_id] = data
    # context['h1'] = "Всякие туры"
    context['page_subtitle'] = dt.subtitle
    context['page_description'] = dt.description
    context['data'] = correct_data
    context['departures_nav'] = dt.departures
    return render(request, "index.html", context=context)


def departure_view(request, departure):
    departure_slug = dt.departures.get(departure, False)
    if departure_slug is False:
        raise Http404('Не найдено направление! ')

    filter_tours = dict([x for x in dt.tours.items() if x[1]['departure'] == departure])
    context = dict()
    context['dep_name'] = dt.departures.get(departure).split(' ')[-1]
    context['cnt_tours'] = len(filter_tours)
    # context['min_price'] = '{:,}'.format(min([filter_tours[x]['price'] for x in filter_tours])).replace(',', ' ')
    # context['max_price'] = '{:,}'.format(max([filter_tours[x]['price'] for x in filter_tours])).replace(',', ' ')
    context['min_price'] = min([filter_tours[x]['price'] for x in filter_tours])
    context['max_price'] = max([filter_tours[x]['price'] for x in filter_tours])
    context['min_date'] = min([filter_tours[x]['nights'] for x in filter_tours])
    context['max_date'] = max([filter_tours[x]['nights'] for x in filter_tours])
    correct_data = {}
    for tour_id, data in filter_tours.items():
        data['card_url'] = data['picture'].replace('&w=800&q=60', '&w=300&h=200')
        # data['price_view'] = '{:,}'.format(data['price']).replace(',', ' ')
        correct_data[tour_id] = data
    context['data'] = correct_data
    context['departures_nav'] = dt.departures
    return render(request, "departure.html", context=context)


def tour_view(request, tour_id):
    tour = dt.tours.get(tour_id, False)
    if tour is False:
        raise Http404('Не найден тур! ')
    stars = [x for x in range(int(tour['stars']))]
    context = tour
    context['rangeSt'] = stars
    # context['price_view'] = '{:,}'.format(context['price']).replace(',', ' ')
    dep_list = dt.departures
    context['dep_name'] = dep_list.get(context.get('departure')).lower()
    context['departures_nav'] = dt.departures
    return render(request, "tour.html", context=context)


def custom_handler404(request, exception):
    # Call when Http404 raised
    return HttpResponseNotFound("{}Выбери из существующих вариантов.".format(exception))


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')
