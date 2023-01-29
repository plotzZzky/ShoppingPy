from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from items.models import Item
from .time import last_day_date, today_date, format_date
from .pantry import get_market_list, get_pharmacy_list


# # # # # # # # # # # # # # Pantry  # # # # # # # # # # # # # #
@login_required()
def view_pantry(request):
    data = {}
    return render(request, 'pantry.html', data)


@login_required()
@csrf_exempt
def get_pantry_list(request, list_id):
    base = request.user.pantry
    today = today_date()
    if list_id == 0:
        result = base.market.all()
    else:
        result = base.pharmacy.all()
    data = {'items': result, 'today': today}
    return render(request, 'pantry_list.html', data)


# # # # # # # # # # # # # # Manage pantry  # # # # # # # # # # # # # #
@login_required()
@csrf_exempt
def add_to_pantry(request, list_id):
    user = request.user
    if list_id == 0:
        get_market_list(user)
    else:
        get_pharmacy_list(user)
    return HttpResponse()


@login_required()
@csrf_exempt
def remove_from_pantry(request, item_id):
    item = Item.objects.get(pk=item_id)  #type: ignore
    item.delete()
    return HttpResponse()


@login_required()
@csrf_exempt
def pantry_clear(request, list_id):
    user = request.user
    if list_id == 0:
        user.pantry.market.clear()
    else:
        user.pantry.pharmacy.clear()
    return HttpResponse()


# # # # # # # # # # # # # # Item properties # # # # # # # # # # # # # #
@login_required()
@csrf_exempt
def get_properties(request, item_id):
    item = Item.objects.get(pk=item_id)  #type: ignore
    data = {'item': item}
    return render(request, 'properties.html', data)


@login_required()
@csrf_exempt
def set_properties(request, item_id, date):
    item = Item.objects.get(pk=item_id)  # type: ignore
    item.date = format_date(date)
    item.alert_date = last_day_date(date, item.validate - 7)
    item.last_day = last_day_date(date, item.validate)
    item.save()
    return HttpResponse()
