from django.test import TestCase
from django.contrib.auth.models import User

from items.models import ItemRef, Item
from users.models import Pantry, List


class PantryTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'zekaka',
            'password': '1234x567'}
        User.objects.create_user(**self.credentials)
        User.objects.create_user(username='temporary', password='1234x567')

    def create_user(self):
        user = User.objects.get(username='temporary')
        pantry = Pantry(user=user)
        pantry.save()
        list_item = List(user=user)
        list_item.save()
        return user

    def create_item(self):
        item_ref = ItemRef(name='arroz', type=0, validate=90)
        item_ref.save()
        item = Item(name='arroz', type=0, amount=1, validate='90', last_day=None)
        item.save()
        return item

    def add_item_to_pantry(self):
        item = self.create_item()
        self.client.get("/list/add/arroz/")
        self.client.get("/pantry/add/id=0/")
        return item

    def test_view_pantry_redirect(self):
        response = self.client.get("/pantry/")
        self.assertEqual(response.status_code, 302)

    def test_view_pantry_success(self):
        self.client.login(**self.credentials)
        response = self.client.get("/pantry/")
        self.assertEqual(response.status_code, 200)

    def test_view_pantry_template(self):
        self.client.login(**self.credentials)
        response = self.client.get("/pantry/")
        self.assertTemplateUsed(response, "pantry.html")

    def test_get_Your_pantry_status(self):
        self.create_user()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get("/pantry/list=0/")
        self.assertEqual(response.status_code, 200)

    def test_get_Your_pantry_template(self):
        self.create_user()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get("/pantry/list=0/")
        self.assertTemplateUsed(response, "pantry_list.html")

    def test_add_item_to_pantry_success(self):
        self.create_user()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get("/pantry/add/id=1/")
        self.assertEqual(response.status_code, 200)

    def test_add_item_to_pantry_error(self):
        self.create_user()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get("/pantry/add/id=99/")
        self.assertEqual(response.status_code, 404)

    def test_remove_to_pantry_success(self):
        self.create_user()
        item = self.add_item_to_pantry()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get(f"/pantry/remove={item.id}/")  # type:ignore
        self.assertEqual(response.status_code, 200)

    def test_remove_to_pantry_result(self):
        self.create_user()
        item = self.add_item_to_pantry()
        self.client.login(username='temporary', password='1234x567')
        self.client.get(f"/pantry/remove={item.id}/")  # type:ignore
        user = User.objects.get(username='temporary')
        response = user.pantry.market.all().count()
        self.assertEqual(response, 0)

    def test_clear_pantry_success(self):
        self.create_user()
        self.add_item_to_pantry()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get(f"/pantry/clear/id=0/")  # type:ignore
        self.assertEqual(response.status_code, 200)

    def test_clear_pantry_result(self):
        self.create_user()
        self.add_item_to_pantry()
        self.client.login(username='temporary', password='1234x567')
        self.client.get(f"/pantry/clear/id=0/")  # type:ignore
        user = User.objects.get(username='temporary')
        response = user.pantry.market.all().count()
        self.assertEqual(response, 0)

    def test_get_props_status(self):
        self.create_user()
        item = self.add_item_to_pantry()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get(f"/pantry/item={item.id}/")  # type:ignore
        self.assertEqual(response.status_code, 200)

    def test_get_props_template(self):
        self.create_user()
        item = self.add_item_to_pantry()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get(f"/pantry/item={item.id}/")  # type:ignore
        self.assertTemplateUsed(response, "properties.html")

    def test_get_props_status_error(self):
        self.create_user()
        item = self.add_item_to_pantry()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get(f"/pantry/item={item.id + 99}/")  # type:ignore
        self.assertEqual(response.status_code, 404)

    def test_post_props_status(self):
        self.create_user()
        item = self.add_item_to_pantry()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get(f"/pantry/item={item.id}/date=2021-12-11/")  # type:ignore
        self.assertEqual(response.status_code, 200)

    def test_post_props_result(self):
        self.create_user()
        item = self.add_item_to_pantry()
        self.client.login(username='temporary', password='1234x567')
        self.client.get(f"/pantry/item={item.id}/date=2021-12-1/")  # type:ignore
        response = Item.objects.get(pk=item.id)  # type:ignore
        self.assertNotEqual(response.buy_date, item.buy_date)
