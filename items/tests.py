from django.test import TestCase
from django.contrib.auth.models import User

from .models import ItemRef, Item
from users.models import Pantry, List
from .forms import ItemForm


class ItemsTest(TestCase):
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

    def test_app_status(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_app_status_200_logged(self):
        self.client.login(**self.credentials)
        response = self.client.get("/list/")
        self.assertEqual(response.status_code, 200)

    def test_app_redirect(self):
        response = self.client.get("/list/")
        self.assertRedirects(response, "/users/login/?next=/list/")

    def test_app_status_logged(self):
        self.client.login(username=self.credentials['username'], password=self.credentials['password'])
        response = self.client.get("/list/")
        self.assertEqual(response.status_code, 200)

    # New item
    def test_get_new_item_status_302(self):
        response = self.client.get("/list/item/new/")
        self.assertEqual(response.status_code, 302)

    def test_get_new_item_status_logged(self):
        self.client.login(**self.credentials)
        response = self.client.get("/list/item/new/")
        self.assertEqual(response.status_code, 404)

    def test_post_new_item_logged_status(self):
        self.client.login(**self.credentials)
        data = {
            'name': 'temporary',
            'type': 'Mercado',
            'validate': 90
        }
        response = self.client.post("/list/item/new/", data)
        self.assertEqual(response.status_code, 302)

    def test_post_new_item_logged_content(self):
        self.client.login(**self.credentials)
        data = {
            'name': 'temporary',
            'type': 'Mercado',
            'validate': 90
        }
        self.client.post("/list/item/new/", data)
        result = ItemRef.objects.get(name=data['name'])  # type:ignore
        self.assertEqual(result.name, data['name'])

    # Get list all
    def test_get_list_all_id_1_logged_status(self):
        self.client.login(**self.credentials)
        response = self.client.get("/list/all/id=1/")
        self.assertEqual(response.status_code, 200)

    def test_get_list_all_id_99_logged_status_error(self):
        self.client.login(**self.credentials)
        response = self.client.get("/list/all/id=99/")
        self.assertEqual(response.status_code, 404)

    def test_get_list_all_id_string_logged_status_error(self):
        self.client.login(**self.credentials)
        response = self.client.get("/list/all/id=x/")
        self.assertEqual(response.status_code, 404)

    def test_get_list_all_logged_template(self):
        self.client.login(**self.credentials)
        response = self.client.get("/list/all/id=1/")
        self.assertTemplateUsed(response, "list_add.html")

    # Get your list
    def test_get_your_list_status(self):
        user = self.create_user()
        self.client.login(username='temporary', password='1234x567')
        User.objects.get(pk=user.id)
        response = self.client.get("/list/your/id=1/")
        self.assertEqual(response.status_code, 200)

    def test_get_your_list_incorrect_id_99_logged_status(self):
        self.client.login(**self.credentials)
        response = self.client.get(f"/list/your/id=99/")
        self.assertEqual(response.status_code, 404)

    def test_get_your_list_incorrect_id_string_logged_status(self):
        self.create_user()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get(f"/list/your/id=x/")
        self.assertEqual(response.status_code, 404)

    # Remove item
    def test_remove_item_status(self):
        self.create_user()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get("/list/remove/id=1/")
        self.assertEqual(response.status_code, 200)

    def test_remove_item_id_empty_status_error(self):
        self.create_user()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get("/list/remove/id=/")
        self.assertEqual(response.status_code, 404)

    def test_remove_item_id_status_error(self):
        self.create_user()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.post("/list/remove/id=9999999/")
        self.assertEqual(response.status_code, 404)

    def test_remove_item_id_string_status_error(self):
        self.create_user()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get("/list/remove/id=xx/")
        self.assertEqual(response.status_code, 404)

    # Add item
    def test_add_item_status(self):
        self.create_user()
        self.create_item()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get("/list/add/arroz/")
        self.assertEqual(response.status_code, 200)

    def test_add_item_empty_status_error(self):
        self.create_user()
        self.create_item()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get("/list/add//")
        self.assertEqual(response.status_code, 404)

    def test_add_item_status_error(self):
        self.create_user()
        self.create_item()
        self.client.login(username='temporary', password='1234x567')
        response = self.client.get("/list/add/nothing/")
        self.assertEqual(response.status_code, 404)

    # Change item
    def test_change_item_amount_status(self):
        self.create_user()
        item = self.create_item()
        self.client.login(username='temporary', password='1234x567')
        self.client.get("/list/add/arroz/")
        response = self.client.get(f"/list/your/{item.id}/amount=5/")  # type:ignore
        self.assertEqual(response.status_code, 200)

    def test_change_item_amount_content(self):
        self.create_user()
        item = self.create_item()
        self.client.login(username='temporary', password='1234x567')
        self.client.get("/list/add/arroz/")
        self.client.get(f"/list/your/{item.id}/amount=5/")  # type:ignore
        response = Item.objects.get(pk=item.id)  # type:ignore
        self.assertEqual(response.amount, 5)

    def test_change_item_amount_status_error(self):
        self.create_user()
        self.create_item()
        self.client.login(username='temporary', password='1234x567')
        self.client.get("/list/add/arroz/")
        response = self.client.get(f"/list/your//amount=5/")  # type:ignore
        self.assertEqual(response.status_code, 404)

    def test_change_item_amount_error_status_error(self):
        self.create_user()
        item = self.create_item()
        self.client.login(username='temporary', password='1234x567')
        self.client.get("/list/add/arroz/")
        response = self.client.get(f"/list/your/{item.id}/amount=xx/")  # type:ignore
        self.assertEqual(response.status_code, 404)

    def test_clear_you_list_status(self):
        self.create_user()
        self.create_item()
        self.client.login(username='temporary', password='1234x567')
        self.client.get("/list/add/arroz/")
        response = self.client.get(f"/list/clear/id=0/")  # type:ignore
        self.assertEqual(response.status_code, 200)

    def test_clear_you_list_content(self):
        user = self.create_user()
        self.create_item()
        self.client.login(username='temporary', password='1234x567')
        self.client.get("/list/add/arroz/")
        self.client.get(f"/list/clear/id=0/")  # type:ignore
        response = List.objects.get(user=user).market.all()  # type:ignore
        self.assertEqual(response.count(), 0)

    def test_clear_you_list_id_empty_status_error(self):
        self.create_user()
        self.create_item()
        self.client.login(username='temporary', password='1234x567')
        self.client.get("/list/add/arroz/")
        response = self.client.get(f"/list/clear/id=/")  # type:ignore
        self.assertEqual(response.status_code, 404)

    def test_clear_you_list_id_error_status_error(self):
        self.create_user()
        self.create_item()
        self.client.login(username='temporary', password='1234x567')
        self.client.get("/list/add/arroz/")
        response = self.client.get(f"/list/clear/id=999/")  # type:ignore
        self.assertEqual(response.status_code, 404)


class FormTest(TestCase):
    def setUp(self):
        pass

    def test_form_sucess(self):
        data = {
            'name': 'temporary',
            'type': 1,
            'validate': 90
        }
        form = ItemForm(data)
        self.assertTrue(form.is_valid())

    def test_form_error_validate_string(self):
        data = {
            'name': 'temporary',
            'type': 1,
            'validate': 'temporary'
        }
        form = ItemForm(data)
        self.assertFalse(form.is_valid())

    def test_form_error_validate_empty(self):
        data = {
            'name': 'temporary',
            'type': 1,
        }
        form = ItemForm(data)
        self.assertFalse(form.is_valid())
