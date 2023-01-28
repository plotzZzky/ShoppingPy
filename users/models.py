from django.db import models
from django.contrib.auth.models import User

from items.models import Item


class List(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    market = models.ManyToManyField(Item, related_name='type_market')
    pharmacy = models.ManyToManyField(Item, related_name='type_pharmacy')


class Pantry(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    market = models.ManyToManyField(Item, related_name='pantry_market')
    pharmacy = models.ManyToManyField(Item, related_name='pantry_pharmacy')
