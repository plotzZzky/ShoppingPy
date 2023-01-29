from items.models import Item


def get_market_list(user):
    user_list = user.list.market.all()
    for item in user_list:
        set_pantry(item, user)
    user.list.market.clear()


def get_pharmacy_list(user):
    user_list = user.list.pharmacy.all()
    for item in user_list:
        set_pantry(item, user)
    user.list.pharmacy.clear()


def set_pantry(item, user):
    if item.amount > 1:
        for x in range(0, item.amount):
            create_item(item, user)
    else:
        create_item(item, user)


def create_item(item, user):
    i = Item(name=item.name, amount=1, type=item.type, validate=item.validate)
    i.save()
    if i.type == '0':
        user.pantry.market.add(i)
    else:
        user.pantry.pharmacy.add(i)
