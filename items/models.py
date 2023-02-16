from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    amount = models.IntegerField()
    validate = models.IntegerField()
    buy_date = models.DateField(null=True, blank=True)
    alert_date = models.DateField(null=True, blank=True)
    last_day = models.DateField(null=True, blank=True)


class ItemRef(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    validate = models.IntegerField()
