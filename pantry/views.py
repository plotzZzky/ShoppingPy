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
    elif list_id == 1:
        result = base.pharmacy.all()
    else:
        return HttpResponse("Pantry dont found", status=404)
    data = {'items': result, 'today': today}
    return render(request, 'pantry_list.html', data)


# # # # # # # # # # # # # # Manage pantry  # # # # # # # # # # # # # #
@login_required()
@csrf_exempt
def add_to_pantry(request, list_id):
    user = request.user
    if list_id == 0:
        get_market_list(user)
    elif list_id == 1:
        get_pharmacy_list(user)
    else:
        return HttpResponse("Item don't found", status=404)
    return HttpResponse("Item added", status=200)


@login_required()
@csrf_exempt
def remove_from_pantry(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)  # type:ignore
        item.delete()
        return HttpResponse("item removed", status=200)
    except Item.DoesNotExist:  # type:ignore
        return HttpResponse("Item dont found", status=404)


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
    try:
        item = Item.objects.get(pk=item_id)  # type:ignore
        data = {'item': item}
        return render(request, 'properties.html', data)
    except Item.DoesNotExist:
        return HttpResponse("Item dont found", status=404)


@login_required()
@csrf_exempt
def set_properties(request, item_id, date):
    try:
        item = Item.objects.get(pk=item_id)  # type: ignore
        item.buy_date = format_date(date)
        item.alert_date = last_day_date(date, item.validate - 7)
        item.last_day = last_day_date(date, item.validate)
        item.save()
        return HttpResponse("Item updated", status=200)
    except Item.DoesNotExist:
        return HttpResponse("Item dont found", status=404)