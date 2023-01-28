from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import ItemForm
from .models import Item, ItemRef


# # # # # # # # # # # # # # List # # # # # # # # # # # # # #
@login_required()
def show_app(request):
    form = ItemForm()
    data = {'form': form}
    return render(request, 'app.html', data)


# # # # # # # # # # # # # # Create Item # # # # # # # # # # # # # #
@login_required()
def create_item(request):
    form = ItemForm(request.POST)
    item = ItemRef.objects.filter(name=request.POST['name']).count()  #type: ignore
    if item == 0:
        if form.is_valid():
            form.save()
    return redirect('/list/')


# # # # # # # # # # # # # # Manage lists  # # # # # # # # # # # # # #
@login_required()
@csrf_exempt
def add_item_to_list(request, name):
    if request.method == 'POST':
        ref = ItemRef.objects.get(name=name)  #type: ignore
        item = Item(name=name, type=ref.type, amount=1, validate=ref.validate, last_day=None)
        item.save()
        if item.type == '0':
            list_item = request.user.list.market
        else:
            list_item = request.user.list.pharmacy
        list_item.add(item)
        return HttpResponse()


@login_required()
@csrf_exempt
def change_amount(request, item_id, amount):
    item = Item.objects.get(pk=item_id)  #type: ignore
    item.amount = amount
    item.save()
    return HttpResponse()


@login_required()
@csrf_exempt
def remove_item_from_list(request, item_id):
    if request.method == 'POST':
        item = Item.objects.get(pk=item_id)  #type: ignore
        item.delete()
    return HttpResponse()


@login_required()
def clear_your_list(request, list_id):
    user = request.user
    if list_id == 0:
        item_list = user.list.market
    else:
        item_list = user.list.pharmacy
    item_list.clear()
    return HttpResponse()


# # # # # # # # # # # # # # Get Lists  # # # # # # # # # # # # # #
@login_required()
def list_all(request, list_id):
    if list_id == 0:
        items = ItemRef.objects.filter(type='0')  #type: ignore
    else:
        items = ItemRef.objects.filter(type='1')  #type: ignore
    data = {'items': items}
    return render(request, 'list_add.html', data)


@login_required()
def get_your_list(request, list_id):
    user = request.user
    if list_id == 0:
        list_items = user.list.market.all()
    else:
        list_items = user.list.pharmacy.all()
    data = {'items': list_items}
    return render(request, 'list_del.html', data)


