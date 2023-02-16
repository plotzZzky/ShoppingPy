from django.test import TestCase
from django.db.utils import IntegrityError

from .models import Item, ItemRef


class ItemTest(TestCase):
    def setUp(self):
        pass

    def test_create_success(self):
        item = Item(
            name='temporary',
            type='temporary',
            amount=1,
            validate=90,
            buy_date="2023-01-12",
            alert_date="2023-01-12",
            last_day="2023-01-12",
        )
        item.save()
        try:
            response = Item.objects.get(name='temporary')  # type:ignore
        except Item.DoesNotExist:  # type:ignore
            response = None
        self.assertIsNotNone(response)

    def test_create_amount_string_error(self):
        try:
            item = Item(
                name='temporary',
                type='temporary',
                amount='xxxx',
                validate=90,
                buy_date="2023-01-12",
                alert_date="2023-01-12",
                last_day="2023-01-12",
            )
            item.save()
            response = Item.objects.get(name='temporary')  # type:ignore
        except ValueError:
            response = None
        self.assertIsNone(response)

    def test_create_validate_string_error(self):
        try:
            item = Item(
                name='temporary',
                type='temporary',
                amount=1,
                validate='xxxx',
                buy_date="2023-01-12",
                alert_date="2023-01-12",
                last_day="2023-01-12",
            )
            item.save()
            response = Item.objects.get(name='temporary')  # type:ignore
        except ValueError:
            response = None
        self.assertIsNone(response)

    def test_create_date_error(self):
        try:
            item = Item(
                name='temporary',
                type='temporary',
                amount=1,
                validate=90,
                buy_date=20230112,
                alert_date="2023-01-12",
                last_day="2023-01-12",
            )
            item.save()
            response = Item.objects.get(name='temporary')  # type:ignore
        except TypeError:
            response = None
        self.assertIsNone(response)

    def test_create_name_empty_error(self):
        try:
            item = Item(
                type='temporary',
                amount=1,
                validate=90,
                buy_date="2023-01-12",
                alert_date="2023-01-12",
                last_day="2023-01-12",
            )
            item.save()
            response = Item.objects.get(type='temporary')  # type:ignore
        except Item.DoesNotExist:  # type:ignore
            response = None
        self.assertIsNotNone(response)

    def test_create_amount_empty_error(self):
        try:
            item = Item(
                name='temporary',
                type='temporary',
                validate=90,
                buy_date="2023-01-12",
                alert_date="2023-01-12",
                last_day="2023-01-12",
            )
            item.save()
            response = Item.objects.get(name='temporary')  # type:ignore
        except IntegrityError:
            response = None
        self.assertIsNone(response)

    def test_create_type_empty_error(self):
        try:
            item = Item(
                name='temporary',
                amount=1,
                validate=90,
                buy_date="2023-01-12",
                alert_date="2023-01-12",
                last_day="2023-01-12",
            )
            item.save()
            response = Item.objects.get(name='temporary')  # type:ignore
        except IntegrityError:
            response = None
        self.assertIsNotNone(response)

    def test_create_validate_empty_error(self):
        try:
            item = Item(
                name='temporary',
                type='temporary',
                amount=1,
                buy_date="2023-01-12",
                alert_date="2023-01-12",
                last_day="2023-01-12",
            )
            item.save()
            response = Item.objects.get(name='temporary')  # type:ignore
        except IntegrityError:
            response = None
        self.assertIsNone(response)


class ItemRefTest(TestCase):
    def setUp(self):
        pass

    def test_create_success(self):
        try:
            item = ItemRef(
                name='temporary',
                type='temporary',
                validate=90
            )
            item.save()
            response = ItemRef.objects.get(name='temporary')  # type:ignore
        except IntegrityError:
            response = None
        self.assertIsNotNone(response)

    def test_create_validate_string_error(self):
        try:
            item = ItemRef(
                name='temporary',
                type='temporary',
                validate='xxx'
            )
            item.save()
            response = ItemRef.objects.get(name='temporary')  # type:ignore
        except ValueError:
            response = None
        self.assertIsNone(response)

    def test_create_validate_empty_error(self):
        try:
            item = ItemRef(
                name='temporary',
                type='temporary',
            )
            item.save()
            response = ItemRef.objects.get(name='temporary')  # type:ignore
        except IntegrityError:
            response = None
        self.assertIsNone(response)

    def test_create_validate_none_error(self):
        try:
            item = ItemRef(
                name='temporary',
                type='temporary',
                validate=None
            )
            item.save()
            response = ItemRef.objects.get(name='temporary')  # type:ignore
        except IntegrityError:
            response = None
        self.assertIsNone(response)
